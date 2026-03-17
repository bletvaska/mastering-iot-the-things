__version__ = '2025.2'
__author__ = 'mirek <miroslav.binas@tuke.sk>'
__all__ = [
    'BaseModel',
    'Field',
    'validator',
]

builtins_type = type


class _MISSING:
    pass


MISSING = _MISSING()


class _Field:
    _is_field = True

    def __init__(self, default, default_factory, type, optional):
        self.default = default
        self.default_factory = default_factory
        self.type = type
        self.optional = optional


def Field(*, default=MISSING, default_factory=MISSING, type=None, optional=False):
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('Cannot specify both default and default_factory.')
    return _Field(default, default_factory, type, optional)


def validator(field):
    def decorator(func):
        class CallableWrapper:
            def __init__(self, f):
                self._func = f
                self._field = field
                self._is_validator = True

            def __call__(self, instance, value):
                return self._func(instance, value)

        return CallableWrapper(func)

    return decorator


class BaseModel:
    @classmethod
    def _build_fields(cls):
        # already built for this specific class
        if '__fields__' in cls.__dict__:
            return

        fields = {}
        annotations = {}
        validators = {}

        for key, value in cls.__dict__.items():
            if key.startswith("__"):
                continue
            if callable(value) and getattr(value, '_is_validator', False):
                validators.setdefault(value._field, []).append(value)
            elif getattr(value, '_is_field', False):
                fields[key] = value
                if value.type is not None:
                    annotations[key] = value.type
                elif value.default is not MISSING:
                    annotations[key] = builtins_type(value.default)
                elif value.default_factory is not MISSING:
                    annotations[key] = builtins_type(value.default_factory())
            elif not callable(value):
                fields[key] = _Field(default=value, default_factory=MISSING,
                                     type=builtins_type(value), optional=False)
                annotations[key] = builtins_type(value)

        setattr(cls, '__fields__', fields)
        setattr(cls, '__annotations__', annotations)
        setattr(cls, '__validators__', validators)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._build_fields()

    def __init__(self, **kwargs):
        self.__class__._build_fields()

        # set field defaults
        for key, field in self.__class__.__fields__.items():
            if field.default is not MISSING:
                object.__setattr__(self, key, field.default)
            elif field.default_factory is not MISSING:
                object.__setattr__(self, key, field.default_factory())

        # apply kwargs through __setattr__ for validation
        for key, value in kwargs.items():
            setattr(self, key, value)

        # check required fields
        for key, field in self.__class__.__fields__.items():
            if field.default is MISSING and field.default_factory is MISSING and key not in kwargs:
                raise TypeError(f'Missing required field "{key}" for {self.__class__.__name__}.')

    def __iter__(self):
        return iter(self.__dict__.items())

    def __setattr__(self, name, value):
        if name not in self.__class__.__fields__:
            raise AttributeError(f'Attribute "{name}" is not in class {self.__class__.__name__}.')

        field = self.__class__.__fields__[name]
        expected_type = self.__class__.__annotations__.get(name)

        # allow None for optional fields
        if value is None and field.optional:
            super().__setattr__(name, value)

        # no type info — skip type check
        elif expected_type is None or expected_type is builtins_type(None):
            super().__setattr__(name, value)

        # if value is a dict, try to construct the expected type from it
        elif isinstance(value, dict):
            super().__setattr__(name, expected_type(**value))

        # type mismatch
        elif not isinstance(value, expected_type):
            raise ValueError(f'Value "{value}" for attribute "{name}" is not of type "{expected_type}".')

        else:
            super().__setattr__(name, value)

        # custom validators
        validators = getattr(self.__class__, "__validators__", {})
        if name in validators:
            for vfunc in validators[name]:
                vfunc(self, value)

    def __repr__(self) -> str:
        items = [f"{key}={repr(value)}" for key, value in self.__dict__.items()]
        return f"{self.__class__.__name__}({','.join(items)})"

    def model_dump(self) -> dict:
        result = {}

        for field, value in self.__dict__.items():
            if isinstance(value, BaseModel):
                result[field] = value.model_dump()
            elif isinstance(value, list):
                result[field] = [
                    entry.model_dump() if isinstance(entry, BaseModel) else entry
                    for entry in value
                ]
            else:
                result[field] = value

        return result
