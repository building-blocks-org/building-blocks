from typing import Generic, Protocol, TypeVar

SourceType = TypeVar("SourceType", contravariant=True)
TargetType = TypeVar("TargetType", covariant=True)


class Mapper(Protocol, Generic[SourceType, TargetType]):  # pragma: no cover
    """
    A generic contract for mapping objects from one representation to another.

    This abstraction can be implemented in any layer of an application—
    for example, it can map:
      - an HTTP request DTO to an internal service request model,
      - a domain entity to a persistence/infrastructure model,
      - a service response to an HTTP response DTO,
      - any source type to any target type.

    Example usages:
      >>> # HTTP request DTO to service request
      >>> class HttpToServiceRequestMapper(Mapper[HttpRequest, ServiceRequest]):
      ...     def map(self, source: HttpRequest) -> ServiceRequest:
      ...         return ServiceRequest(id=source.id, data=source.body)

      >>> # Domain entity to infrastructure model
      >>> class DomainToPersistenceMapper(Mapper[User, UserRecord]):
      ...     def map(self, source: User) -> UserRecord:
      ...         return UserRecord(pk=source.user_id, name=source.name)
    """

    def map(self, source: SourceType) -> TargetType:
        """
        Map a source object of type SourceType to a target object of type TargetType.
        Args:
            source (SourceType): The source object to be mapped.
        Returns:
            TargetType: The mapped target object.
        """
        ...
