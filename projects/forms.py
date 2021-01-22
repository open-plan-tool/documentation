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


economic_widgets = {
    'discount': forms.NumberInput(attrs={'placeholder': 'eg. 0.1', 'min':'0.0', 'max':'1.0', 'step':'0.0001',
                                            'title': 'Investment Discount factor.'}),
    'tax': forms.NumberInput(attrs={'placeholder': 'eg. 0.3', 'min':'0.0', 'max':'1.0', 'step':'0.0001'}),
}

class EconomicDataUpdateForm(ModelForm):
    class Meta:
        model = EconomicData
        fields = '__all__'
        widgets = economic_widgets


class ProjectCreateForm(forms.Form):
    name = forms.CharField(label='Project Name', widget=forms.TextInput(attrs={'placeholder': 'Name...', 'data-toggle': 'tooltip', 'title': 'A self explanatory name for the project.'}))
    description = forms.CharField(label='Project Description',
                                  widget=forms.Textarea(attrs={'placeholder': 'More detailed description here...', 'data-toggle': 'tooltip', 'title': 'A description of what this project objectives or test cases.'}))
    country = forms.ChoiceField(label='Country', choices=COUNTRY,
        widget=forms.Select(attrs={'data-toggle': 'tooltip', 'title': 'Name of the country where the project is being deployed'}))
    longitude = forms.FloatField(label='Location, longitude',
                                 widget=forms.NumberInput(attrs={'placeholder': 'click on the map', 'readonly': '', 
                                 'data-toggle': 'tooltip', 'title': " Longitude coordinate of the project's geographical location."}))
    latitude = forms.FloatField(label='Location, latitude',
                                widget=forms.NumberInput(attrs={'placeholder': 'click on the map', 'readonly': '',
                                'data-toggle': 'tooltip', 'title': "Latitude coordinate of the project's geographical location."}))
    duration = forms.IntegerField(label='Project Duration (years)',
                                  widget=forms.NumberInput(attrs={'placeholder': 'eg. 1 ', 'min':'0', 'max':'100', 'step':'1', 'data-toggle': 'tooltip', 
                                  'title': "The number of years the project is intended to be operational. The project duration also sets the installation time of the assets used in the simulation. After the project ends these assets are 'sold' and the refund is charged against the initial investment costs."}))
    currency = forms.ChoiceField(label='Currency', choices=CURRENCY,
        widget=forms.Select(attrs={'data-toggle': 'tooltip', 'title': 'The currency of the country where the project is implemented.'}))
    discount = forms.FloatField(label='Discount Factor',
                                  widget=forms.NumberInput(attrs={'placeholder': 'eg. 0.1', 'min':'0.0', 'max':'1.0', 'step':'0.0001',
                                  'data-toggle': 'tooltip', 'title': 'Discount factor is the factor which accounts for the depreciation in the value of money in the future, compared to the current value of the same money. The common method is to calculate the weighted average cost of capital (WACC) and use it as the discount rate.'}))
    tax = forms.FloatField(label='Tax',
                             widget=forms.NumberInput(attrs={'placeholder': 'eg. 0.3', 'min':'0.0', 'max':'1.0', 'step':'0.0001',
                             'data-toggle': 'tooltip', 'title': 'Tax factor.'}))
    
    electricity = forms.BooleanField(label='Electricity', initial=False, required=False)
    heat = forms.BooleanField(label='Heat', initial=False, required=False)
    gas = forms.BooleanField(label='Gas', initial=False, required=False)
    h2 = forms.BooleanField(label='H2', initial=False, required=False)
    diesel = forms.BooleanField(label='Diesel', initial=False, required=False)

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


class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['date_created', 'date_updated', 'economic_data', 'user']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['id', 'project']



# region Scenarion

scenario_widgets = {
    'name': forms.TextInput(attrs={'placeholder': 'Scenario name'}),
    'start_date': forms.DateInput(format='%m/%d/%Y',
                                  attrs={'class': 'TestDateClass', 'placeholder': 'Select a start date'}),
    'time_step': forms.NumberInput(attrs={'placeholder': 'eg. 120 minutes', 'data-toggle': 'tooltip',
                                          'title': 'Length of the time-steps.'}),
    'evaluated_period': forms.NumberInput(attrs={'placeholder': 'eg. 10 days', 'data-toggle': 'tooltip',
                                                 'title': 'The number of days for which the simulation is to be run.'}),
    'capex_fix': forms.NumberInput(attrs={'placeholder': 'e.g. 10000€', 'data-toggle': 'tooltip',
                                          'title': ' A fixed cost to implement the asset, eg. planning costs which do not depend on the (optimized) asset capacity.'}),
    'capex_var': forms.NumberInput(attrs={'placeholder': 'e.g. 1000€', 'data-toggle': 'tooltip',
                                          'title': ' Actual CAPEX of the asset, i.e., specific investment costs'}),
    'opex_fix': forms.NumberInput(attrs={'placeholder': 'e.g. 0€', 'data-toggle': 'tooltip',
                                         'title': 'Actual OPEX of the asset, i.e., specific operational and maintenance costs.'}),
    'opex_var': forms.NumberInput(attrs={'placeholder': 'e.g. 0.6€/kWh', 'data-toggle': 'tooltip',
                                         'title': 'Variable cost associated with a flow through/from the asset (currency/kWh).'}),
}

scenario_labels = {
    "name": "Name",
    'evaluated_period': "Evaluated Period (days)",
    "time_step": "Time Step (minutes)",
    "start_date": "Start Date",
    "capex_fix": "Development costs (currency)",
    "capex_var": "Specific costs (currency)",
    "opex_fix": "Specific OM costs (currency)",
    "opex_var": "Dispatch price (currency/kWh)",
}


class ScenarioCreateForm(ModelForm):
    #start_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Scenario
        exclude = ['id', 'project']
        widgets = scenario_widgets
        labels = scenario_labels


class ScenarioUpdateForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ['id', 'project']
        widgets = scenario_widgets
        labels = scenario_labels

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False  # don't include <form> tag
        # self.helper.layout = Layout(
        #     Row(Column('name', css_class='form-group col-xs-5'),
        #         Column('start_date', css_class='form-group col-xs-4'),
        #         css_class='form-row row'),
        #     Row(Column('time_step', css_class='form-group col-xs-5'),
        #         Column('evaluated_period', css_class='form-group col-xs-4'),
        #         css_class='form-row row'),
        #     Row(Column('capex_fix', css_class='form-group col-xs-2'),
        #         Column('capex_var', css_class='form-group col-xs-2'),
        #         Column('opex_fix', css_class='form-group col-xs-2'),
        #         Column('opex_var', css_class='form-group col-xs-3'),
        #         css_class='form-row row'),
        # )


class LoadScenarioFromFileForm(BSModalModelForm):
    class Meta:
        model = ScenarioFile
        fields = ['title', 'file']
# endregion Scenario


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
            'optimize_cap': forms.Select(choices=TRUE_FALSE_CHOICES,
                                         attrs={'data-toggle': 'tooltip', 'title': 'True if the user wants to perform capacity optimization for various components as part of the simulation.',
                                                'style': 'font-weight:400; font-size:13px; height:40px;'}),
            'dispatchable': forms.Select(choices=TRUE_FALSE_CHOICES),
            'renewable_asset': forms.Select(choices=TRUE_FALSE_CHOICES),

            'name': forms.TextInput(attrs={'placeholder': 'Asset Name',
                                           'style': 'font-weight:400; font-size:13px;'}),
            'time_step': forms.NumberInput(attrs={'placeholder': 'eg. 120 minutes',
                                                  'data-toggle': 'tooltip', 'title': 'Length of the time-steps.',
                                                  'style': 'font-weight:400; font-size:13px;'}),
            'capex_fix': forms.NumberInput(attrs={'placeholder': 'e.g. 10000',
                                                  'data-toggle': 'tooltip', 'title': ' A fixed cost to implement the asset, eg. planning costs which do not depend on the (optimized) asset capacity.',
                                                  'style': 'font-weight:400; font-size:13px;'}),
            'capex_var': forms.NumberInput(attrs={'placeholder': 'e.g. 4000',
                                                  'data-toggle': 'tooltip', 'title': ' Actual CAPEX of the asset, i.e., specific investment costs',
                                                  'style': 'font-weight:400; font-size:13px;'}),
            'opex_fix': forms.NumberInput(attrs={'placeholder': 'e.g. 0',
                                                 'data-toggle': 'tooltip', 'title': 'Actual OPEX of the asset, i.e., specific operational and maintenance costs.',
                                                 'style': 'font-weight:400; font-size:13px;'}),
            'opex_var': forms.NumberInput(attrs={'placeholder': 'Currency',
                                                 'data-toggle': 'tooltip', 'title': 'Variable cost associated with a flow through/from the asset (currency/kWh).',
                                                 'style': 'font-weight:400; font-size:13px;'}),
            'lifetime': forms.NumberInput(attrs={'placeholder': 'e.g. 10 years',
                                                 'data-toggle': 'tooltip', 'title': 'Number of operational years of the asset until it has to be replaced.',
                                                 'style': 'font-weight:400; font-size:13px;'}),
            'input_timeseries': forms.Textarea(attrs={'placeholder': 'e.g. [4,3,2,5,3,...]',
                                                      'style': 'font-weight:400; font-size:13px;'}),
            'crate': forms.NumberInput(attrs={'placeholder': 'factor of total capacity (kWh), e.g. 0.7',
                                              'data-toggle': 'tooltip', 'title': 'C-rate is the rate at which the storage can charge or discharge relative to the nominal capacity of the storage. A c-rate of 1 implies that the battery can discharge or charge completely in a single timestep.',
                                              'style': 'font-weight:400; font-size:13px;'}),
            'efficiency': forms.NumberInput(attrs={'placeholder': 'e.g. 0.99',
                                                   'data-toggle': 'tooltip', 'title': 'Ratio of energy output/energy input.',
                                                   'style': 'font-weight:400; font-size:13px;', 'min': '0.0', 'max': '1.0', 'step': '.0001'}),
            'soc_initial': forms.NumberInput(attrs={'placeholder': 'e.g. 2',
                                                    'data-toggle': 'tooltip', 'title': 'The level of charge (as a factor of the actual capacity) in the storage in the zeroth time-step.',
                                                    'style': 'font-weight:400; font-size:13px;'}),
            'soc_max': forms.NumberInput(attrs={'placeholder': 'e.g. 190',
                                                'data-toggle': 'tooltip', 'title': 'The maximum permissible level of charge in the battery (generally, it is when the battery is filled to its nominal capacity), represented by the value 1.0. Users can  also specify a certain value as a factor of the actual capacity.',
                                                'style': 'font-weight:400; font-size:13px;'}),
            'soc_min': forms.NumberInput(attrs={'placeholder': 'e.g. 20',
                                                'data-toggle': 'tooltip', 'title': 'The minimum permissible level of charge in the battery as a factor of the nominal capacity of the battery.',
                                                'style': 'font-weight:400; font-size:13px;'}),
            'maximum_capacity': forms.NumberInput(attrs={'placeholder': 'e.g. 1000',
                                                         'data-toggle': 'tooltip', 'title': 'The maximum installable capacity.',
                                                         'style': 'font-weight:400; font-size:13px;'}),
            'energy_price': forms.NumberInput(attrs={'placeholder': 'e.g. 0.1',
                                                     'data-toggle': 'tooltip', 'title': 'Price of electricity sourced from the utility grid.',
                                                     'style': 'font-weight:400; font-size:13px;'}),
            'feedin_tariff': forms.NumberInput(attrs={'placeholder': 'e.g. 0.0',
                                                      'data-toggle': 'tooltip', 'title': 'Price received for feeding electricity into the grid.',
                                                      'style': 'font-weight:400; font-size:13px;'}),
            'peak_demand_pricing': forms.NumberInput(attrs={'placeholder': 'e.g. 60',
                                                            'data-toggle': 'tooltip', 'title': 'Price to be paid additionally for energy-consumption based on the peak demand of a period.',
                                                            'style': 'font-weight:400; font-size:13px;'}),
            'peak_demand_pricing_period': forms.NumberInput(attrs={'placeholder': 'times per year, e.g. 2',
                                                                   'data-toggle': 'tooltip', 'title': 'Number of reference periods in one year for the peak demand pricing. Only one of the following are acceptable values: 1 (yearly), 2, 3 ,4, 6, 12 (monthly).',
                                                                   'style': 'font-weight:400; font-size:13px;', 'min': '1', 'max': '12', 'step': '1'}),
            'renewable_share': forms.NumberInput(attrs={'placeholder': 'e.g. 0.1',
                                                        'data-toggle': 'tooltip', 'title': 'The share of renewables in the generation mix of the energy supplied by the DSO (utility).',
                                                        'style': 'font-weight:400; font-size:13px;'}),
            'installed_capacity': forms.NumberInput(attrs={'placeholder': 'e.g. 50',
                                                           'data-toggle': 'tooltip', 'title': 'The already existing installed capacity in-place, which will also be replaced after its lifetime.',
                                                           'style': 'font-weight:400; font-size:13px;'}),
            'age_installed': forms.NumberInput(attrs={'placeholder': 'e.g. 10',
                                                      'data-toggle': 'tooltip', 'title': 'The number of years the asset has already been in operation.',
                                                      'style': 'font-weight:400; font-size:13px;'}),
        }
        labels = {
            "name": "Name",
            "optimize_cap": "Optimize cap",
            "dispatchable": "Dispatchable",
            "renewable_asset": "Renewable asset",
            "capex_fix": "Development costs (currency)",
            "capex_var": "Specific costs (currency)",
            "opex_fix": "Specific OM costs (currency)",
            "opex_var": "Dispatch price (currency/kWh)",
            "lifetime": "Asset Lifetime (years)",
            "input_timeseries": "Timeseries vector",
            "crate": "Crate",
            "efficiency": "Efficiency",
            "soc_initial": "SoC initial",
            "soc_max": "SoC max",
            "soc_min": "SoC min",
            "maximum_capacity": "Maximum capacity",
            "energy_price": "Energy price (currency/kWh)",
            "feedin_tariff": "Feedin tariff (currency/kWh)",
            "peak_demand_pricing": "Peak demand pricing (currency/kW)",
            "peak_demand_pricing_period": "Peak demand pricing period (times/year)",
            "renewable_share": "Renewable share",
            "installed_capacity": "installed capacity (kW)",
            "age_installed": "Age installed (years)",
        }
