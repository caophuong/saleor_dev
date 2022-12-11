# Generated by Django 3.2.6 on 2021-08-25 10:29
from django.apps import apps as registry
from django.db import migrations
from django.db.models.signals import post_migrate


def assing_permissions(apps, schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        Group = apps.get_model("auth", "Group")
        Permission = apps.get_model("auth", "Permission")
        ContentType = apps.get_model("contenttypes", "ContentType")

        ct, _ = ContentType.objects.get_or_create(app_label="account", model="user")
        impersonate_user, _ = Permission.objects.get_or_create(
            name="Impersonate user.", content_type=ct, codename="impersonate_user"
        )

        manage_users = Permission.objects.filter(
            codename="manage_users", content_type__app_label="account"
        )

        for group in Group.objects.filter(permissions__in=manage_users).iterator():
            group.permissions.add(impersonate_user)

    sender = registry.get_app_config("account")
    post_migrate.connect(on_migrations_complete, weak=False, sender=sender)


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0054_alter_user_language_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ("email",),
                "permissions": (
                    ("manage_users", "Manage customers."),
                    ("manage_staff", "Manage staff."),
                    ("impersonate_user", "Impersonate user."),
                ),
            },
        ),
        migrations.RunPython(assing_permissions, migrations.RunPython.noop),
    ]