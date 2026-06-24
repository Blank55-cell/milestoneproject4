from django.core.management.base import BaseCommand
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = "Mark all existing email addresses as verified"

    def handle(self, *args, **kwargs):
        updated = 0
        for email in EmailAddress.objects.filter(verified=False):
            email.verified = True
            email.primary = True
            email.save()
            updated += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Verified: {email.email}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {updated} accounts verified."
            )
        )
