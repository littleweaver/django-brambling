from django.conf.urls import patterns, url, include
from django.templatetags.static import static
from django.views.generic.base import TemplateView, RedirectView

from brambling.forms.user import (
    FloppyAuthenticationForm,
    FloppyPasswordResetForm,
    FloppySetPasswordForm,
)
from brambling.models import Discount
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
    UserDashboardView,
    SplashView,
    InviteAcceptView,
    InviteSendView,
    InviteDeleteView,
)
from brambling.views.organizer import (
    EventCreateView,
    EventSummaryView,
    EventUpdateView,
    StripeConnectView,
    RemoveEditorView,
    PublishEventView,
    UnpublishEventView,
    ItemListView,
    item_form,
    DiscountListView,
    discount_form,
    AttendeeFilterView,
    OrderFilterView,
    OrganizerApplyDiscountView,
    RemoveDiscountView,
    OrderDetailView,
    RefundView,
    TogglePaymentConfirmationView,
)
from brambling.views.payment import (
    EventDwollaConnectView,
    OrderDwollaConnectView,
    UserDwollaConnectView,
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
from brambling.views.utils import split_view


urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('brambling/favicon.ico'))),

    url(r'^$',
        split_view(lambda r, *a, **k: r.user.is_authenticated(),
                   UserDashboardView.as_view(),
                   SplashView.as_view()),
        name="brambling_dashboard"),
    url(r'^create/$',
        EventCreateView.as_view(),
        name="brambling_event_create"),
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
    url(r'^profile/card/add/$',
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

    url(r'^(?P<event_slug>[\w-]+)/$',
        RedirectView.as_view(pattern_name="brambling_event_order_summary", permanent=False),
        name="brambling_event_root"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?shop/$',
        ChooseItemsView.as_view(),
        name="brambling_event_shop"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?add/(?P<pk>\d+)/$',
        AddToOrderView.as_view(),
        name="brambling_event_shop_add"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?remove/(?P<pk>\d+)/$',
        RemoveFromOrderView.as_view(),
        name="brambling_event_shop_remove"),

    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?attendees/$',
        AttendeesView.as_view(),
        name="brambling_event_attendee_list"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?attendees/(?P<pk>\d+)/$',
        AttendeeBasicDataView.as_view(),
        name="brambling_event_attendee_edit"),

    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?housing_data/$',
        AttendeeHousingView.as_view(),
        name='brambling_event_attendee_housing'),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?survey/$',
        SurveyDataView.as_view(),
        name='brambling_event_survey'),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?hosting/$',
        HostingView.as_view(),
        name='brambling_event_hosting'),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?email/$',
        OrderEmailView.as_view(),
        name="brambling_event_order_email"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{8})/)?summary/$',
        SummaryView.as_view(),
        name="brambling_event_order_summary"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?:(?P<code>[a-zA-Z0-9]{{8}})/)?discount/use/(?P<discount>{})/$'.format(Discount.CODE_REGEX),
        ApplyDiscountView.as_view(),
        name="brambling_event_use_discount"),
    url(r'^(?P<event_slug>[\w-]+)/order/(?P<code>[a-zA-Z0-9]{8})/dwolla_connect/$',
        OrderDwollaConnectView.as_view(),
        name="brambling_order_dwolla_connect"),

    url(r'^(?P<slug>[\w-]+)/summary/$',
        EventSummaryView.as_view(),
        name="brambling_event_summary"),
    url(r'^(?P<slug>[\w-]+)/edit/$',
        EventUpdateView.as_view(),
        name="brambling_event_update"),
    url(r'^(?P<slug>[\w-]+)/dwolla_connect/$',
        EventDwollaConnectView.as_view(),
        name="brambling_event_dwolla_connect"),
    url(r'^(?P<event_slug>[\w-]+)/remove_editor/(?P<pk>\d+)$',
        RemoveEditorView.as_view(),
        name="brambling_event_remove_editor"),
    url(r'^(?P<event_slug>[\w-]+)/publish/$',
        PublishEventView.as_view(),
        name="brambling_event_publish"),
    url(r'^(?P<event_slug>[\w-]+)/unpublish/$',
        UnpublishEventView.as_view(),
        name="brambling_event_unpublish"),
    url(r'^(?P<event_slug>[\w-]+)/items/$',
        ItemListView.as_view(),
        name="brambling_item_list"),
    url(r'^(?P<event_slug>[\w-]+)/items/create/$',
        item_form,
        name="brambling_item_create"),
    url(r'^(?P<event_slug>[\w-]+)/items/(?P<pk>\d+)/$',
        item_form,
        name="brambling_item_update"),
    url(r'^(?P<event_slug>[\w-]+)/attendees/$',
        AttendeeFilterView.as_view(),
        name="brambling_event_attendees"),
    url(r'^(?P<event_slug>[\w-]+)/orders/$',
        OrderFilterView.as_view(),
        name="brambling_event_orders"),
    url(r'^(?P<event_slug>[\w-]+)/orders/(?P<code>[a-zA-Z0-9]{8})/$',
        OrderDetailView.as_view(),
        name="brambling_event_order_detail"),
    url(r'^(?P<event_slug>[\w-]+)/orders/(?P<code>[a-zA-Z0-9]{8})/remove_discount/(?P<discount_pk>\d+)/$',
        RemoveDiscountView.as_view(),
        name="brambling_event_remove_discount"),
    url(r'^(?P<event_slug>[\w-]+)/orders/(?P<code>[a-zA-Z0-9]{8})/apply_discount/$',
        OrganizerApplyDiscountView.as_view(),
        name="brambling_event_apply_discount"),
    url(r'^(?P<event_slug>[\w-]+)/orders/(?P<code>[a-zA-Z0-9]{8})/refund/$',
        RefundView.as_view(),
        name="brambling_event_refund"),
    url(r'^(?P<event_slug>[\w-]+)/orders/(?P<code>[a-zA-Z0-9]{8})/confirm/(?P<payment_pk>\d+)/$',
        TogglePaymentConfirmationView.as_view(),
        name="brambling_event_toggle_payment_confirmation"),

    url(r'^(?P<event_slug>[\w-]+)/discount/$',
        DiscountListView.as_view(),
        name="brambling_discount_list"),
    url(r'^(?P<event_slug>[\w-]+)/discount/create/$',
        discount_form,
        name="brambling_discount_create"),
    url(r'^(?P<event_slug>[\w-]+)/discount/(?P<pk>\d+)/$',
        discount_form,
        name="brambling_discount_update"),
)
