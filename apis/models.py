# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Fundingrounds2(models.Model):
    logo = models.CharField(db_column='Logo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    industry = models.CharField(db_column='Industry', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=255, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ceo = models.CharField(db_column='CEO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=255, blank=True, null=True)  # Field name made lowercase.
    linkedin = models.CharField(db_column='LinkedIn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c_facebook = models.CharField(max_length=255, blank=True, null=True)
    c_twitter = models.CharField(max_length=255, blank=True, null=True)
    c_linkedin = models.CharField(max_length=255, blank=True, null=True)
    c_location = models.CharField(max_length=255, blank=True, null=True)
    c_founders = models.CharField(max_length=255, blank=True, null=True)
    c_phone = models.CharField(max_length=255, blank=True, null=True)
    c_email = models.CharField(max_length=255, blank=True, null=True)
    c_description = models.TextField(blank=True, null=True)
    c_employees = models.CharField(max_length=255, blank=True, null=True)
    c_founded = models.CharField(max_length=255, blank=True, null=True)
    revenu_range = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FundingRounds2'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Companies(models.Model):
    country = models.TextField(blank=True, null=True)
    founded = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    linkedin_url = models.TextField(blank=True, null=True)
    locality = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    size = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companies'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Fundingrounds(models.Model):
    logo = models.CharField(db_column='Logo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    industry = models.CharField(db_column='Industry', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=255, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ceo = models.TextField(db_column='CEO', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=255, blank=True, null=True)  # Field name made lowercase.
    linkedin = models.CharField(db_column='LinkedIn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c_facebook = models.CharField(max_length=255, blank=True, null=True)
    c_twitter = models.CharField(max_length=255, blank=True, null=True)
    c_linkedin = models.CharField(max_length=255, blank=True, null=True)
    c_location = models.CharField(max_length=255, blank=True, null=True)
    c_founders = models.CharField(max_length=255, blank=True, null=True)
    c_phone = models.CharField(max_length=255, blank=True, null=True)
    c_email = models.TextField(blank=True, null=True)
    c_description = models.TextField(blank=True, null=True)
    c_title = models.TextField(blank=True, null=True)
    c_employees = models.CharField(max_length=255, blank=True, null=True)
    c_founded = models.CharField(max_length=255, blank=True, null=True)
    revenu_range = models.CharField(max_length=255, blank=True, null=True)
    privacy_link = models.TextField(db_column='Privacy_link', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fundingrounds'


class News(models.Model):
    company_id = models.IntegerField()
    company_name = models.CharField(max_length=250)
    articles = models.TextField()
    date = models.CharField(max_length=255)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    image = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Refreshtokens(models.Model):
    token = models.CharField(max_length=255, blank=True, null=True)
    expirydate = models.DateTimeField(db_column='expiryDate', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'refreshTokens'


class Role(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'role'


class Roles(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles'


class TechsFunding(models.Model):
    id_fund = models.IntegerField(unique=True)
    techs = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'techs_funding'


class UserEmailNotify(models.Model):
    user_email = models.CharField(unique=True, max_length=255)
    industry = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_email_notify'


class UserRoles(models.Model):
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    roleid = models.OneToOneField(Role, models.DO_NOTHING, db_column='roleId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_roles'
        unique_together = (('roleid', 'userid'),)


class Users(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    authtoken = models.CharField(db_column='authToken', max_length=255)  # Field name made lowercase.
    paid = models.CharField(max_length=1)
    deactivate = models.IntegerField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'


class WordsTag(models.Model):
    url = models.CharField(max_length=255)
    words_tags = models.TextField()

    class Meta:
        managed = False
        db_table = 'words_tag'
