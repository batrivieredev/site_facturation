# Import all models here for Alembic autogeneration
from .user import User, Role
from .client import Client
from .appointment import Appointment, AppointmentType
from .invoice import Invoice, InvoiceItem
from .payment import Payment
from .setting import Setting
from .mail_setting import MailSetting
from .mail_log import MailLog
from .agenda_link import AgendaLink
