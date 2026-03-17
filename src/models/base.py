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
    """Define a model field with extended metadata.

    Used as a class-level default in BaseModel subclasses to provide type
    information, default values, and validation behaviour that cannot be
    expressed with a plain assignment.

    Args:
        default: Default value for the field. Mutually exclusive with
                 default_factory.
        default_factory: A callable invoked on each instantiation to produce
                         the default value. Use for mutable defaults such as
                         lists or nested models.
        type: Expected type or tuple of types for runtime type checking.
              Required when the default is None and type inference is not
              possible.
        optional: If True, None is accepted as a valid value regardless of
                  the declared type.

    Raises:
        ValueError: If both default and default_factory are provided.

    Example:
        class Settings(BaseModel):
            broker: str = Field(default='localhost', type=str)
            port: int = Field(default=1883, type=int)
            tags: list = Field(default_factory=list)
            token: str = Field(default=None, type=str, optional=True)
            timeout: int = Field(type=int)  # required field
    """
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('Cannot specify both default and default_factory.')
    return _Field(default, default_factory, type, optional)


def validator(field: str):
    """Decorator that registers a method as a field validator.

    The decorated method is called after each assignment to the specified
    field. It receives the model instance and the new value as arguments.
    Raise an exception inside the validator to reject the value.

    Args:
        field: Name of the field to validate.

    Example:
        class Sensor(BaseModel):
            temperature: float = 0.0

            @validator('temperature')
            def validate_temperature(self, value):
                if value < -273.15:
                    raise ValueError('Temperature below absolute zero.')
    """
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
    """Lightweight data model base class for MicroPython.

    Provides dataclass-like behaviour with runtime type checking, field
    validation, and serialisation. Designed as a minimal alternative to
    pydantic for use in resource-constrained environments.

    Fields are declared as class-level attributes. Plain assignments infer
    the type from the default value. Use Field() for advanced configuration
    such as optional fields, explicit types, or mutable defaults.

    Field metadata is built once per class via _build_fields(), called
    automatically on first instantiation or via __init_subclass__ when
    supported by the runtime.

    Example:
        class WiFi(BaseModel):
            ssid: str = Field(default=None, type=str, optional=True)
            password: str = Field(default=None, type=str, optional=True)

        class Settings(BaseModel):
            wifi: WiFi = Field(default_factory=WiFi, type=WiFi)
            retries: int = 3

        s = Settings(retries=5)
        s.retries = 'x'  # raises ValueError
    """
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
