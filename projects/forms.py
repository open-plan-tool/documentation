from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Field, Fieldset, ButtonHolder
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
                                 widget=forms.NumberInput(attrs={'placeholder': 'eg. -77.0364', 'readonly': ''}))
    latitude = forms.FloatField(label='Location, latitude',
                                widget=forms.NumberInput(attrs={'placeholder': 'eg. 38.8951', 'readonly': ''}))
    duration = forms.IntegerField(label='Project Duration (years)',
                                  widget=forms.NumberInput(attrs={'placeholder': 'eg. 1 '}))
    currency = forms.ChoiceField(label='Currency', choices=CURRENCY)
    discount = forms.FloatField(label='Discount Factor',
                                  widget=forms.NumberInput(attrs={'placeholder': 'eg. 0.1'}))
    tax = forms.FloatField(label='Tax',
                             widget=forms.NumberInput(attrs={'placeholder': 'eg. 0.3'}))
    #annuity_factor = forms.FloatField(label='Annuity Factor', widget=forms.NumberInput(attrs={'placeholder': 'Annuity Factor...'}))
    #crf = forms.FloatField(label='CRF', widget=forms.NumberInput(attrs={'placeholder': 'CRF...'}))

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
        self.helper.label_class = 'col-lg-8'
        self.helper.field_class = 'col-lg-10'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['id', 'project']


class ScenarioCreateForm(ModelForm):
    #start_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Scenario
        exclude = ['id', 'project']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of Scenario'}),
            'start_date': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'TestDateClass', 'placeholder': 'Select a start date'}),
            'time_step': forms.NumberInput(attrs={'placeholder': 'eg. 120 minutes'}),
            'evaluated_period': forms.NumberInput(attrs={'placeholder': 'eg. 10 days'}),
            'capex_fix': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'capex_var': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'opex_fix': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'opex_var': forms.NumberInput(attrs={'placeholder': 'Currency'}),
        }
        labels = {
            "name": "Name",
            'evaluated_period': "Evaluated Period (days)",
            "time_step": "Time Step (minutes)",
            "capex_fix": "Fixed Capital Expenses",
            "start_date": "Start Date",
        }


class ScenarioUpdateForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ['id', 'project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False  # don't include <form> tag
        self.helper.layout = Layout(
            Row(Column('name', css_class='form-group col-xs-5'),
                Column('start_date', css_class='form-group col-xs-4'),
                css_class='form-row row'),
            Row(Column('time_step', css_class='form-group col-xs-5'),
                Column('evaluated_period', css_class='form-group col-xs-4'),
                css_class='form-row row'),
            Row(Column('capex_fix', css_class='form-group col-xs-2'),
                Column('capex_var', css_class='form-group col-xs-2'),
                Column('opex_fix', css_class='form-group col-xs-2'),
                Column('opex_var', css_class='form-group col-xs-3'),
                css_class='form-row row'),

        )


class LoadScenarioFromFileForm(BSModalModelForm):
    class Meta:
        model = ScenarioFile
        fields = ['title', 'file']


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
        widgets = {
            'optimize_cap': forms.Select(choices=TRUE_FALSE_CHOICES),
            'dispatchable': forms.Select(choices=TRUE_FALSE_CHOICES),
            'renewable_asset': forms.Select(choices=TRUE_FALSE_CHOICES),

            'name': forms.TextInput(attrs={'placeholder': 'Unique name',
                                           'data-toggle': 'tooltip', 'title': 'Add tooltip content here!'}),
            'time_step': forms.NumberInput(attrs={'placeholder': 'eg. 120 minutes'}),
            'capex_fix': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'capex_var': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'opex_fix': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'opex_var': forms.NumberInput(attrs={'placeholder': 'Currency'}),
            'lifetime': forms.NumberInput(attrs={'placeholder': 'e.g. 10 years'}),
            'input_timeseries': forms.Textarea(attrs={'placeholder': 'e.g. [4,3,2,5,3,...]'}),
            'crate': forms.NumberInput(attrs={'placeholder': 'e.g. 0.7'}),
            'efficiency': forms.NumberInput(attrs={'placeholder': 'e.g. 0.99'}),
            'self_discharge': forms.NumberInput(attrs={'placeholder': 'e.g. 3'}),
            'soc_initial': forms.NumberInput(attrs={'placeholder': 'e.g. 2'}),
            'soc_max': forms.NumberInput(attrs={'placeholder': 'e.g. 190'}),
            'soc_min': forms.NumberInput(attrs={'placeholder': 'e.g. 20'}),
            'maximum_capacity': forms.NumberInput(attrs={'placeholder': 'e.g. 200'}),
            'energy_price': forms.NumberInput(attrs={'placeholder': 'e.g. 42'}),
            'feedin_tariff': forms.NumberInput(attrs={'placeholder': 'e.g. 0.5'}),
            'peak_demand_pricing': forms.NumberInput(attrs={'placeholder': 'e.g. 5'}),
            'peak_demand_pricing_period': forms.NumberInput(attrs={'placeholder': 'e.g. 2'}),
            'renewable_share': forms.NumberInput(attrs={'placeholder': 'e.g. 0.7'}),
            'installed_capacity': forms.NumberInput(attrs={'placeholder': 'e.g. 100'}),
            'age_installed': forms.NumberInput(attrs={'placeholder': 'e.g. 10'}),
        }
        labels = {
            "name": "Name",
            "optimize_cap": "Optimize cap",
            "dispatchable": "Dispatchable",
            "renewable_asset": "Renewable asset",
            "capex_fix": "Development costs",
            "capex_var": "Specific costs",
            "opex_fix": "Specific OM costs",
            "opex_var": "Dispatch price",
            "lifetime": "Asset Lifetime",
            "input_timeseries": "Timeseries vector",
            "crate": "Crate",
            "efficiency": "Efficiency",
            "self_discharge": "Self discharge",
            "soc_initial": "SoC initial",
            "soc_max": "SoC max",
            "soc_min": "SoC min",
            "maximum_capacity": "Maximum capacity",
            "energy_price": "Energy price",
            "feedin_tariff": "Feedin tariff",
            "peak_demand_pricing": "Peak demand pricing",
            "peak_demand_pricing_period": "Peak demand pricing period",
            "renewable_share": "Renewable share",
            "installed_capacity": "installed capacity (kW)",
            "age_installed": "Age installed",
        }
