from rest_framework import serializers

from brambling.models import (Order, Person, EventHousing, BoughtItem,
                              EnvironmentalFactor, HousingCategory,
                              ItemOption, Item, ItemImage, Attendee, Event,
                              Organization, DanceStyle)


class HousingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingCategory
        fields = ('id', 'name')


class EnvironmentalFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalFactor
        fields = ('id', 'name')


class DanceStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanceStyle
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id', 'given_name', 'middle_name', 'surname', 'name_order',
        )


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes public data for an organization."""
    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'slug', 'description', 'website_url', 'facebook_url',
            'banner_image', 'city', 'state_or_province', 'country',
            'dance_styles',
        )


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes public data for an event."""
    class Meta:
        model = Event
        fields = (
            'id', 'name', 'slug', 'description', 'website_url', 'facebook_url',
            'banner_image', 'city', 'state_or_province', 'country',
            'start_date', 'end_date', 'start_time', 'end_time', 'dance_styles',
            'has_dances', 'has_classes', 'liability_waiver', 'organization',
        )


class AttendeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendee
        fields = (
            'id', 'order', 'given_name', 'middle_name', 'surname',
            'name_order', 'basic_completed', 'email', 'phone',
            'liability_waiver', 'photo_consent', 'housing_status',
            'housing_completed', 'nights', 'ef_cause', 'ef_avoid',
            'person_prefer', 'person_avoid', 'housing_prefer',
            'housing_avoid', 'other_needs',
        )


class EventHousingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventHousing
        fields = (
            'id', 'event', 'order', 'contact_name', 'contact_email',
            'contact_phone', 'address', 'address_2', 'city',
            'state_or_province', 'zip_code', 'country',
            'public_transit_access', 'ef_present', 'ef_avoid', 'person_prefer',
            'person_avoid', 'housing_categories',
        )


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    bought_items = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='boughtitem-detail',
        queryset=BoughtItem.objects.all(),
    )
    eventhousing = serializers.HyperlinkedRelatedField(
        view_name='eventhousing-detail',
        queryset=EventHousing.objects.all(),
    )

    class Meta:
        model = Order
        fields = (
            'id', 'event', 'person', 'email', 'code', 'cart_start_time',
            'bought_items', 'survey_completed', 'heard_through', 'heard_through_other',
            'send_flyers', 'send_flyers_address', 'send_flyers_address_2',
            'send_flyers_city', 'send_flyers_state_or_province',
            'send_flyers_zip', 'send_flyers_country', 'providing_housing',
            'notes', 'eventhousing',
        )

    def to_representation(self, obj):
        data = super(OrderSerializer, self).to_representation(obj)
        # Workaround for https://github.com/SmileyChris/django-countries/issues/106
        if data['send_flyers_country'] == '':
            data['send_flyers_country'] = ''
        return data


class BoughtItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BoughtItem
        fields = (
            'id', 'item_option', 'order', 'added', 'status', 'attendee'
        )


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'event', 'created',
                  'last_modified')


class ItemImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('id', 'item', 'order', 'image')


class ItemOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemOption
        fields = ('id', 'item', 'name', 'price', 'total_number',
                  'available_start', 'available_end', 'remaining_display',
                  'order')
