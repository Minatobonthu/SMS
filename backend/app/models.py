from enum import unique
from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ForeignKey

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key = True, nullable=False)
    email_address = Column(String, nullable = False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    account_status = Column(String, nullable=False)
    failed_attempts = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    created_by = Column(String, nullable=False)
    last_modified_by = Column(String, nullable=False)

  
class Organization(Base):
    __tablename__ = "school"
    organization_id = Column(Integer, primary_key = True, nullable=False)
    unique_school_id = Column(String,unique=True, nullable=False)
    school_name = Column(String, nullable=False)
    school_address = Column(String, nullable=False)
    principal_name = Column(String, nullable=False)
    head_master = Column(String)
    phone_number = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("now()"))
    created_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)
    last_modified_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)

class Organization_access(Base):
    __tablename__ = "schoolaccess"
    organization_access_id = Column(Integer, primary_key = True, nullable=False)
    organization_id = Column(Integer, ForeignKey("school.organization_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("now()"))
    created_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)
    last_modified_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)


class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key = True, nullable=False)
    role_name = Column(String, nullable=False, unique=True )
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("now()"))
    created_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)
    last_modified_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)

class RoleAccess(Base):
    __tablename__ = "rolesaccess"
    roleaccess_id = Column(Integer, primary_key = True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("now()"))
    created_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)
    last_modified_by = Column(Integer,  ForeignKey("users.user_id", ondelete= "CASCADE"), nullable=False)


  