from django.conf.urls import patterns, url, include
from django.http import HttpResponse
from django.templatetags.static import static
from django.views.generic.base import TemplateView, RedirectView

from brambling.forms.user import (
    FloppyAuthenticationForm,
    FloppyPasswordResetForm,
    FloppySetPasswordForm,
)
from brambling.forms.organizer import (
    OrganizationProfileForm,
)
from brambling.models import Discount
from brambling.views.orders import (
    AddToOrderView,
    RemoveFromOrderView,
    ApplyDiscountView,
    ChooseItemsView,
    AttendeeBasicDataView,
    AttendeesView,
    SurveyDataView,
    HostingView,
    OrderEmailView,
    SummaryView,
    TransferView,
    RactiveShopView,
    OrderCodeRedirectView,
)
from brambling.views.core import (
    ExceptionView,
    DashboardView,
)
from brambling.views.invites import (
    InviteAcceptView,
    InviteSendView,
    InviteDeleteView,
)
from brambling.views.mail import (
    ConfirmationPreviewView,
    OrderReceiptPreviewView,
    OrderAlertPreviewView,
    InvitePreviewView,
    DailyDigestPreviewView,
)
from brambling.views.organizer import (
    OrganizationUpdateView,
    OrganizationPermissionsView,
    OrganizationPaymentView,
    OrganizationDetailView,
    OrganizationRemoveEditorView,
    OrderRedirectView,
    EventCreateView,
    EventSummaryView,
    EventBasicSettingsView,
    EventDesignView,
    EventPermissionsView,
    EventRegistrationView,
    StripeConnectView,
    EventRemoveMemberView,
    PublishEventView,
    UnpublishEventView,
    DangerZoneView,
    ItemListView,
    item_form,
    ItemDeleteView,
    DiscountListView,
    discount_form,
    CustomFormListView,
    custom_form_form,
    AttendeeFilterView,
    OrderFilterView,
    OrderDetailView,
    RefundView,
    TogglePaymentConfirmationView,
    SendReceiptView,
    FinancesView,
)
from brambling.views.payment import (
    DwollaConnectView,
    DwollaWebhookView,
)
from brambling.views.user import (
    AccountView,
    NotificationsView,
    BillingView,
    HomeView,
    SignUpView,
    EmailConfirmView,
    send_confirmation_email_view,
    CreditCardAddView,
    CreditCardDeleteView,
    ClaimOrdersView,
    ClaimOrderView,
    MergeOrderView,
    OrderHistoryView,
    SavedAttendeesView,
    SavedAttendeeManageView,
    SavedAttendeeDeleteView,
    OrganizeEventsView,
    OrganizeOrganizationsView,
)


order_urlpatterns = patterns('',
    url(r'^ractive-shop/$', RactiveShopView.as_view()),
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
    url(r'^attendees/add/$',
        AttendeeBasicDataView.as_view(),
        name="brambling_event_attendee_add"),
    url(r'^attendees/(?P<pk>\d+)/$',
        AttendeeBasicDataView.as_view(),
        name="brambling_event_attendee_edit"),

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
    url(r'^transfer/$',
        TransferView.as_view(),
        name="brambling_event_order_transfer"),
)


event_urlpatterns = patterns('',
    url(r'^$',
        RedirectView.as_view(pattern_name="brambling_event_order_summary", permanent=False),
        name="brambling_event_root"),

    url(r'^order/', include(order_urlpatterns)),
    url(r'^order/(?P<code>[a-zA-Z0-9]{8})/',
        OrderCodeRedirectView.as_view(),
        name='brambling_order_code_redirect'),
    url(r'^summary/$',
        EventSummaryView.as_view(),
        name="brambling_event_summary"),
    url(r'^basic/$',
        EventBasicSettingsView.as_view(),
        name="brambling_event_basic"),
    url(r'^design/$',
        EventDesignView.as_view(),
        name="brambling_event_design"),
    url(r'^permissions/$',
        EventPermissionsView.as_view(),
        name="brambling_event_permissions"),
    url(r'^registration/$',
        EventRegistrationView.as_view(),
        name="brambling_event_registration"),
    url(r'^remove_member/(?P<pk>\d+)$',
        EventRemoveMemberView.as_view(),
        name="brambling_event_remove_member"),
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
    url(r'^items/(?P<pk>\d+)/delete/$',
        ItemDeleteView.as_view(),
        name="brambling_item_delete"),
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

    url(r'^danger-zone/$',
        DangerZoneView.as_view(),
        name="brambling_event_danger_zone"),
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
    url(r'^edit/permissions/$',
        OrganizationPermissionsView.as_view(),
        name='brambling_organization_update_permissions'),
    url(r'^edit/payment/$',
        OrganizationPaymentView.as_view(),
        name='brambling_organization_update_payment'),
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
    url(r'^dwolla_connect/$',
        DwollaConnectView.as_view(),
        name="brambling_dwolla_connect"),

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

    url(r'^account/$',
        AccountView.as_view(),
        name="brambling_user_account"),
    url(r'^notifications/$',
        NotificationsView.as_view(),
        name="brambling_user_notifications"),
    url(r'^billing/$',
        BillingView.as_view(),
        name="brambling_user_billing"),
    url(r'^billing/card/add/(?P<api_type>test|live)/$',
        CreditCardAddView.as_view(),
        name="brambling_user_card_add"),
    url(r'^billing/card/delete/(?P<pk>\d+)/$',
        CreditCardDeleteView.as_view(),
        name="brambling_user_card_delete"),
    url(r'^attendees/$',
        SavedAttendeesView.as_view(),
        name="brambling_user_attendees"),
    url(r'^attendees/add/$',
        SavedAttendeeManageView.as_view(),
        name="brambling_user_attendee_add"),
    url(r'^attendees/(?P<pk>\d+)/$',
        SavedAttendeeManageView.as_view(),
        name="brambling_user_attendee_edit"),
    url(r'^attendees/(?P<pk>\d+)/delete/$',
        SavedAttendeeDeleteView.as_view(),
        name="brambling_user_attendee_remove"),
    url(r'^home/$',
        HomeView.as_view(),
        name="brambling_home"),
    url(r'^history/$',
        OrderHistoryView.as_view(),
        name="brambling_order_history"),
    url(r'^claim-orders/$',
        ClaimOrdersView.as_view(),
        name="brambling_claim_orders"),
    url(r'^claim-orders/(?P<pk>\d+)/$',
        ClaimOrderView.as_view(),
        name="brambling_claim_order"),
    url(r'^merge-order/$',
        MergeOrderView.as_view(),
        name="brambling_merge_order"),
    url(r'^events/$',
        OrganizeEventsView.as_view(),
        name="brambling_organize_events"),
    url(r'^organizations/$',
        OrganizeOrganizationsView.as_view(),
        name="brambling_organize_organizations"),

    url(r'^daguerre/', include('daguerre.urls')),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^418/$', TemplateView.as_view(template_name='418.html')),
    url(r'^500/$', 'django.views.defaults.server_error'),
    url(r'^500/raise/$', ExceptionView.as_view()),
    url(r'^ping/$', lambda r: HttpResponse('A-Okay!')),
    url(r'^mail/confirmation/$', ConfirmationPreviewView.as_view()),
    url(r'^mail/order_receipt/$', OrderReceiptPreviewView.as_view()),
    url(r'^mail/order_alert/$', OrderAlertPreviewView.as_view()),
    url(r'^mail/invite_event/$', InvitePreviewView.as_view(kind='event')),
    url(r'^mail/invite_event_edit/$', InvitePreviewView.as_view(kind='event_edit')),
    url(r'^mail/invite_event_view/$', InvitePreviewView.as_view(kind='event_view')),
    url(r'^mail/invite_org_owner/$', InvitePreviewView.as_view(kind='org_owner')),
    url(r'^mail/invite_org_edit/$', InvitePreviewView.as_view(kind='org_edit')),
    url(r'^mail/invite_org_view/$', InvitePreviewView.as_view(kind='org_view')),
    url(r'^mail/invite_transfer/$', InvitePreviewView.as_view(kind='transfer')),
    url(r'^mail/daily_digest/$', DailyDigestPreviewView.as_view()),

    url(r'^webhooks/dwolla/$', DwollaWebhookView.as_view(), name='brambling_dwolla_webhook'),

    url(r'^api/', include('brambling.api.urls')),

    url(r'^create/$',
        EventCreateView.as_view(),
        name="brambling_event_create"),

    url(r'^(?P<organization_slug>[\w-]+)/', include(organization_urlpatterns)),
)
