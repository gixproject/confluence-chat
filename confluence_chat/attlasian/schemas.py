import datetime

from pydantic import Field, BaseModel


class ConfluenceWorkSpaceDescriptionSchema(BaseModel):
    plain: dict
    view: dict


class ConfluenceWorkSpaceIconSchema(BaseModel):
    path: str
    apiDownloadLink: str | None = None


class ConfluenceWorkSpaceLinks(BaseModel):
    webui: str


class ConfluenceWorkSpaceSchema(BaseModel):
    id: int
    key: str
    name: str
    type: str
    status: str
    authorId: str
    createdAt: datetime.datetime
    homepageId: int
    description: ConfluenceWorkSpaceDescriptionSchema | None = None
    icon: ConfluenceWorkSpaceIconSchema | None = None
    links: ConfluenceWorkSpaceLinks = Field(alias="_links")


class ConfluencePageVersionSchema(BaseModel):
    createdAt: str
    message: str
    number: int
    minorEdit: bool
    authorId: str


class ConfluencePageBodyStorageSchema(BaseModel):
    representation: str
    value: str


class ConfluencePageBodySchema(BaseModel):
    storage: ConfluencePageBodyStorageSchema


class ConfluencePageSchemaLinks(BaseModel):
    webui: str
    editui: str
    tinyui: str


class ConfluencePageSchema(BaseModel):
    id: str
    status: str
    title: str
    spaceId: str
    parentId: str | None
    parentType: str | None
    position: int
    authorId: str
    ownerId: str
    lastOwnerId: str | None
    createdAt: str
    version: ConfluencePageVersionSchema | None
    body: ConfluencePageBodySchema
    links: ConfluencePageSchemaLinks = Field(alias="_links")
