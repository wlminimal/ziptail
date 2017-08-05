from __future__ import absolute_import, unicode_literals

from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from modelcluster.fields import ParentalKey

from .forms import SubscriptionForm
from mailchimp3 import MailChimp


class HomePage(Page):

    def serve(self, request):
        if request.method == "POST":
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['number']
                area = phone_number[0:3]
                head = phone_number[3:6]
                tail = phone_number[6:]
                pnumber_format = '{}-{}-{}'.format(area, head, tail)

                # Subscribe to Mailchimp List
                client = MailChimp(
                    settings.MAILCHIMP_USERNAME,
                    settings.MAILCHIMP_API_KEY
                )
                client.lists.members.create(
                    settings.MAILCHIMP_LIST_ID,
                    {
                        'email_address': email,
                        'status': 'subscribed',
                        'merge_fields': {
                            'PNUMBER': pnumber_format
                        }
                    }
                )
                return HttpResponseRedirect('thank-you')
        else:
            form = SubscriptionForm()

        return render(
            request,
            self.template,
            {
                'page': self,
                'form': form,
            }
        )


class ThankYouPage(Page):
    thank_you_text = models.CharField(
        max_length=255,
        default="Thank you for Subscription"
    )

    content_panels = Page.content_panels + [
        FieldPanel('thank_you_text'),
    ]
