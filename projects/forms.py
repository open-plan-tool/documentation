from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm

from projects.models import *



class ProjectDetailForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['date_created', 'date_updated', 'economic_data', 'user']

    def __init__(self, *args, **kwargs):
        super(ProjectDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class EconomicDataDetailForm(ModelForm):
    class Meta:
        model = EconomicData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EconomicDataDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['date_created', 'date_updated', 'economic_data', 'user']


class EconomicDataUpdateForm(ModelForm):
    class Meta:
        model = EconomicData
        fields = '__all__'


class ProjectCreateForm(forms.Form):
    name = forms.CharField(label='Project Name', widget=forms.TextInput(attrs={'placeholder': 'Name...'}))
    description = forms.CharField(label='Project Description',
                                  widget=forms.Textarea(attrs={'placeholder': 'More detailed description here...'}))

    country = forms.ChoiceField(label='Country', choices=COUNTRY)
    longitude = forms.FloatField(label='Location, longitude',
                                 widget=forms.NumberInput(attrs={'placeholder': 'longitude...'}))
    latitude = forms.FloatField(label='Location, latitude',
                                widget=forms.NumberInput(attrs={'placeholder': 'latitude...'}))
    duration = forms.IntegerField(label='Project Duration',
                                  widget=forms.NumberInput(attrs={'placeholder': 'Project Duration...'}))
    currency = forms.ChoiceField(label='Currency', choices=CURRENCY)
    discount = forms.IntegerField(label='Discount Factor',
                                  widget=forms.NumberInput(attrs={'placeholder': 'Discount Factor...'}))
    tax = forms.IntegerField(label='Tax',
                             widget=forms.NumberInput(attrs={'placeholder': 'Tax...'}))

    electricity = forms.BooleanField(label='Electricity', initial=False, required=False)
    heat = forms.BooleanField(label='Heat', initial=False, required=False)
    gas = forms.BooleanField(label='Gas (LNG)', initial=False, required=False)
    h2 = forms.BooleanField(label='H2', initial=False, required=False)
    mobility = forms.BooleanField(label='Electric Mobility', initial=False, required=False)

    # Render form
    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'project_form_id'
        # self.helper.form_class = 'blueForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['id', 'project']


class ScenarioCreateForm(ModelForm):
    start_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Scenario
        exclude = ['id', 'project']


class ScenarioUpdateForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ['id', 'project']


class AssetCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetCreateForm, self).__init__(*args, **kwargs)
        ''' DrawFlow specific configuration, add a special attribute to 
            every field in order for the framework to be able to export
            the data to json.
            !! This addition doesn't affect the previous behavior !!
        '''
        for field in self.fields:
            self.fields[field].widget.attrs.update({f'df-{field}': ''})
        ''' ----------------------------------------------------- '''

    class Meta:
        model = Asset
        exclude = ['scenario']
