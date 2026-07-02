from typing import Optional
import datetime
import decimal

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import CHAR, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


# email, hashed_password, is_active, is_superuser, is_verified come from SQLAlchemyBaseUserTable.
# ponytail: base declares email as varchar(320)/hashed_password as varchar(1024); DB is 100/255.
# Only matters for create_all (which we don't run) — runtime maps fine to the existing columns.
class UserProfiles(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user_profiles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_profiles_pkey'),
        UniqueConstraint('email', name='user_profiles_email_key'),
        UniqueConstraint('username', name='user_profiles_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    email_imports: Mapped[list['EmailImports']] = relationship('EmailImports', back_populates='user')
    transactions: Mapped[list['Transactions']] = relationship('Transactions', back_populates='user')


class EmailImports(Base):
    __tablename__ = 'email_imports'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user_profiles.id'], ondelete='CASCADE', name='email_imports_user_id_fkey'),
        PrimaryKeyConstraint('id', name='email_imports_pkey'),
        UniqueConstraint('message_id', name='email_imports_message_id_key'),
        Index('idx_email_imports_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    message_id: Mapped[str] = mapped_column(String(255), nullable=False)
    sender: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    user: Mapped['UserProfiles'] = relationship('UserProfiles', back_populates='email_imports')
    transactions: Mapped[list['Transactions']] = relationship('Transactions', back_populates='email_import')


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        CheckConstraint('amount > 0::numeric', name='transactions_amount_check'),
        CheckConstraint("direction::text = ANY (ARRAY['CREDIT'::character varying, 'DEBIT'::character varying]::text[])", name='transactions_direction_check'),
        CheckConstraint("source::text = ANY (ARRAY['EMAIL'::character varying, 'MANUAL'::character varying]::text[])", name='transactions_source_check'),
        ForeignKeyConstraint(['email_import_id'], ['email_imports.id'], ondelete='SET NULL', name='transactions_email_import_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['user_profiles.id'], ondelete='CASCADE', name='transactions_user_id_fkey'),
        PrimaryKeyConstraint('id', name='transactions_pkey'),
        Index('idx_transactions_date', 'transaction_date'),
        Index('idx_transactions_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    account_name: Mapped[str] = mapped_column(String(100), nullable=False)
    transaction_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    counter_party: Mapped[Optional[str]] = mapped_column(String(100))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    email_import_id: Mapped[Optional[int]] = mapped_column(Integer)

    email_import: Mapped[Optional['EmailImports']] = relationship('EmailImports', back_populates='transactions')
    user: Mapped['UserProfiles'] = relationship('UserProfiles', back_populates='transactions')
