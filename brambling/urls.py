from django.conf.urls import patterns, url, include
from django.templatetags.static import static
from django.views.generic.base import TemplateView, RedirectView

from brambling.forms.user import (
    FloppyAuthenticationForm,
    FloppyPasswordResetForm,
    FloppySetPasswordForm,
)
from brambling.forms.organizer import (
    OrganizationPermissionForm,
    OrganizationProfileForm,
    OrganizationEventDefaultsForm,
)
from brambling.models import Discount, Invite
from brambling.views.orders import (
    AddToOrderView,
    RemoveFromOrderView,
    ApplyDiscountView,
    ChooseItemsView,
    AttendeeBasicDataView,
    AttendeesView,
    AttendeeHousingView,
    SurveyDataView,
    HostingView,
    OrderEmailView,
    SummaryView,
)
from brambling.views.core import (
    ExceptionView,
    DashboardView,
    InviteAcceptView,
    InviteSendView,
    InviteDeleteView,
)
from brambling.views.mail import (
    ConfirmationPreviewView,
    OrderReceiptPreviewView,
    OrderAlertPreviewView,
    InvitePreviewView
)
from brambling.views.organizer import (
    OrganizationUpdateView,
    OrganizationPaymentView,
    OrganizationDetailView,
    OrganizationRemoveEditorView,
    OrderRedirectView,
    EventCreateView,
    EventSummaryView,
    EventUpdateView,
    StripeConnectView,
    EventRemoveEditorView,
    PublishEventView,
    UnpublishEventView,
    ItemListView,
    item_form,
    DiscountListView,
    discount_form,
    CustomFormListView,
    custom_form_form,
    AttendeeFilterView,
    OrderFilterView,
    OrganizerApplyDiscountView,
    RemoveDiscountView,
    OrderDetailView,
    RefundView,
    TogglePaymentConfirmationView,
    SendReceiptView,
    FinancesView,
)
from brambling.views.payment import (
    OrganizationDwollaConnectView,
    OrderDwollaConnectView,
    UserDwollaConnectView,
    DwollaWebhookView,
)
from brambling.views.user import (
    PersonView,
    HomeView,
    RemoveResidentView,
    SignUpView,
    EmailConfirmView,
    send_confirmation_email_view,
    CreditCardAddView,
    CreditCardDeleteView,
)


order_urlpatterns = patterns('',
    url(r'^shop/$',
        ChooseItemsView.as_view(),
        name="brambling_event_shop"),
    url(r'^add/(?P<pk>\d+)/$',
        AddToOrderView.as_view(),
        name="brambling_event_shop_add"),
    url(r'^remove/(?P<pk>\d+)/$',
        RemoveFromOrderView.as_view(),
        name="brambling_event_shop_remove"),

    url(r'^attendees/$',
        AttendeesView.as_view(),
        name="brambling_event_attendee_list"),
    url(r'^attendees/(?P<pk>\d+)/$',
        AttendeeBasicDataView.as_view(),
        name="brambling_event_attendee_edit"),

    url(r'^housing_data/$',
        AttendeeHousingView.as_view(),
        name='brambling_event_attendee_housing'),
    url(r'^survey/$',
        SurveyDataView.as_view(),
        name='brambling_event_survey'),
    url(r'^hosting/$',
        HostingView.as_view(),
        name='brambling_event_hosting'),
    url(r'^email/$',
        OrderEmailView.as_view(),
        name="brambling_event_order_email"),
    url(r'^summary/$',
        SummaryView.as_view(),
        name="brambling_event_order_summary"),
    url(r'^use-discount/(?P<discount>{})/$'.format(Discount.CODE_REGEX),
        ApplyDiscountView.as_view(),
        name="brambling_event_use_discount"),
    url(r'^dwolla_connect/$',
        OrderDwollaConnectView.as_view(),
        name="brambling_order_dwolla_connect"),
)


event_urlpatterns = patterns('',
    url(r'^$',
        RedirectView.as_view(pattern_name="brambling_event_order_summary", permanent=False),
        name="brambling_event_root"),

    url(r'^order/(?:(?P<code>[a-zA-Z0-9]{8})/)?', include(order_urlpatterns)),
    url(r'^summary/$',
        EventSummaryView.as_view(),
        name="brambling_event_summary"),
    url(r'^edit/$',
        EventUpdateView.as_view(),
        name="brambling_event_update"),
    url(r'^remove_editor/(?P<pk>\d+)$',
        EventRemoveEditorView.as_view(),
        name="brambling_event_remove_editor"),
    url(r'^publish/$',
        PublishEventView.as_view(),
        name="brambling_event_publish"),
    url(r'^unpublish/$',
        UnpublishEventView.as_view(),
        name="brambling_event_unpublish"),
    url(r'^items/$',
        ItemListView.as_view(),
        name="brambling_item_list"),
    url(r'^items/create/$',
        item_form,
        name="brambling_item_create"),
    url(r'^items/(?P<pk>\d+)/$',
        item_form,
        name="brambling_item_update"),
    url(r'^attendees/$',
        AttendeeFilterView.as_view(),
        name="brambling_event_attendees"),
    url(r'^finances/$',
        FinancesView.as_view(),
        name="brambling_event_finances"),
    url(r'^orders/$',
        OrderFilterView.as_view(),
        name="brambling_event_orders"),
    url(r'^orders/(?P<code>[a-zA-Z0-9]{8})/$',
        OrderDetailView.as_view(),
        name="brambling_event_order_detail"),
    url(r'^orders/(?P<code>[a-zA-Z0-9]{8})/remove_discount/(?P<discount_pk>\d+)/$',
        RemoveDiscountView.as_view(),
        name="brambling_event_remove_discount"),
    url(r'^orders/(?P<code>[a-zA-Z0-9]{8})/apply_discount/$',
        OrganizerApplyDiscountView.as_view(),
        name="brambling_event_apply_discount"),
    url(r'^orders/(?P<code>[a-zA-Z0-9]{8})/refund/(?P<pk>\d+)/$',
        RefundView.as_view(),
        name="brambling_event_refund"),
    url(r'^orders/(?P<code>[a-zA-Z0-9]{8})/confirm/(?P<payment_pk>\d+)/$',
        TogglePaymentConfirmationView.as_view(),
        name="brambling_event_toggle_payment_confirmation"),
    url(r'^orders/(?P<code>[a-zA-Z0-9]{8})/send_receipt/$',
        SendReceiptView.as_view(),
        name="brambling_event_send_receipt"),

    url(r'^discount/$',
        DiscountListView.as_view(),
        name="brambling_discount_list"),
    url(r'^discount/create/$',
        discount_form,
        name="brambling_discount_create"),
    url(r'^discount/(?P<pk>\d+)/$',
        discount_form,
        name="brambling_discount_update"),

    url(r'^forms/$',
        CustomFormListView.as_view(),
        name="brambling_form_list"),
    url(r'^forms/create/$',
        custom_form_form,
        name="brambling_form_create"),
    url(r'^forms/(?P<pk>\d+)/$',
        custom_form_form,
        name="brambling_form_update"),
)


organization_urlpatterns = patterns('',
    url(r'^$',
        OrganizationDetailView.as_view(),
        name='brambling_organization_detail'),
    url(r'^edit/profile/$',
        OrganizationUpdateView.as_view(
            form_class=OrganizationProfileForm,
            template_name='brambling/organization/profile.html',
        ),
        name='brambling_organization_update'),
    url(r'^edit/event_defaults/$',
        OrganizationUpdateView.as_view(
            form_class=OrganizationEventDefaultsForm,
            template_name='brambling/organization/event_defaults.html'
        ),
        name='brambling_organization_update_event_defaults'),
    url(r'^edit/permissions/$',
        OrganizationUpdateView.as_view(
            form_class=OrganizationPermissionForm,
            template_name='brambling/organization/permissions.html'
        ),
        name='brambling_organization_update_permissions'),
    url(r'^edit/payment/$',
        OrganizationPaymentView.as_view(),
        name='brambling_organization_update_payment'),
    url(r'^create/$',
        EventCreateView.as_view(),
        name="brambling_event_create"),
    url(r'^dwolla_connect/$',
        OrganizationDwollaConnectView.as_view(),
        name="brambling_organization_dwolla_connect"),
    url(r'^remove_editor/(?P<pk>\d+)$',
        OrganizationRemoveEditorView.as_view(),
        name="brambling_organization_remove_editor"),

    url(r'^order/(?:(?P<code>[a-zA-Z0-9]{8})/)?', OrderRedirectView.as_view()),

    url(r'^(?P<event_slug>[\w-]+)/', include(event_urlpatterns)),
)


urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('brambling/favicon.ico'))),

    url(r'about/', TemplateView.as_view(template_name='brambling/about.html'), name='brambling_about'),
    url(r'faq/', TemplateView.as_view(template_name='brambling/faq.html'), name='brambling_faq'),
    url(r'pricing/', TemplateView.as_view(template_name='brambling/pricing.html'), name='brambling_pricing'),
    url(r'global/', TemplateView.as_view(template_name='brambling/global.html'), name='brambling_global'),

    url(r'^$',
        DashboardView.as_view(),
        name="brambling_dashboard"),
    url(r'^stripe_connect/$',
        StripeConnectView.as_view(),
        name="brambling_stripe_connect"),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'authentication_form': FloppyAuthenticationForm},
        name='login'),
    url(r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        {'password_reset_form': FloppyPasswordResetForm},
        name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'set_password_form': FloppySetPasswordForm},
        name='password_reset_confirm'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^signup/$',
        SignUpView.as_view(),
        name="brambling_signup"),
    url(r'^email_confirm/send/$',
        send_confirmation_email_view,
        name="brambling_email_confirm_send"),
    url(r'^email_confirm/(?P<pkb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        EmailConfirmView.as_view(),
        name="brambling_email_confirm"),
    url(r'^invite/(?P<code>[a-zA-Z0-9~-]{20})/$',
        InviteAcceptView.as_view(),
        name="brambling_invite_accept"),
    url(r'^invite/(?P<code>[a-zA-Z0-9~-]{20})/send/$',
        InviteSendView.as_view(),
        name="brambling_invite_send"),
    url(r'^invite/(?P<code>[a-zA-Z0-9~-]{20})/delete/$',
        InviteDeleteView.as_view(),
        name="brambling_invite_delete"),

    url(r'^profile/$',
        PersonView.as_view(),
        name="brambling_user_profile"),
    url(r'^profile/card/add/(?P<api_type>test|live)/$',
        CreditCardAddView.as_view(),
        name="brambling_user_card_add"),
    url(r'^profile/card/delete/(?P<pk>\d+)/$',
        CreditCardDeleteView.as_view(),
        name="brambling_user_card_delete"),
    url(r'^profile/dwolla_connect/$',
        UserDwollaConnectView.as_view(),
        name="brambling_user_dwolla_connect"),
    url(r'^home/$',
        HomeView.as_view(),
        name="brambling_home"),
    url(r'^home/remove_resident/(?P<pk>\d+)/$',
        RemoveResidentView.as_view(),
        name='brambling_home_remove_resident'),

    url(r'^daguerre/', include('daguerre.urls')),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^418/$', TemplateView.as_view(template_name='418.html')),
    url(r'^500/$', 'django.views.defaults.server_error'),
    url(r'^500/raise/$', ExceptionView.as_view()),
    url(r'^mail/confirmation/$', ConfirmationPreviewView.as_view()),
    url(r'^mail/order_receipt/$', OrderReceiptPreviewView.as_view()),
    url(r'^mail/order_alert/$', OrderAlertPreviewView.as_view()),
    url(r'^mail/invite_home/$', InvitePreviewView.as_view(kind=Invite.HOME)),
    url(r'^mail/invite_event/$', InvitePreviewView.as_view(kind=Invite.EVENT_EDITOR)),
    url(r'^mail/invite_org/$', InvitePreviewView.as_view(kind=Invite.ORGANIZATION_EDITOR)),

    url(r'^webhooks/dwolla/$', DwollaWebhookView.as_view(), name='brambling_dwolla_webhook'),

    url(r'^(?P<organization_slug>[\w-]+)/', include(organization_urlpatterns)),
)
