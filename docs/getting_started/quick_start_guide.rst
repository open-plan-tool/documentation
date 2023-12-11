===========
Quick start
===========

First steps
-----------

CREATE AN ACCOUNT
^^^^^^^^^^^^^^^^
The first step to start using open-plan-tool is to create an account. To do this, you must click on the "Sign up" button at the top right corner and fill in the following information: your name, email address, username and password. Finally, do not forget to read and accept the privacy statement. You should receive an email with a link to confirm the account creation.


.. image:: ../images/IMG1_Sign_up.png
 :width: 100%

EXPLORE THE DASHBOARD
^^^^^^^^^^^^^^^^^^^^

When you log in, the following dashboard is displayed. In the following image the points described below are labeled with numbers and letters.

.. image:: ../images/IMG2_Main_Screen.png
 :width: 100%

**1. Logo. Clicking here will take you back to the home screen.**

**2. Top navigation menu. Located on the upper right part of the screen, here you will find the shortcuts to:**

    a) Simulation results. Visualize the results of your scenarios in this tab.
    b) New scenario. Your projects can be composed of multiple scenarios and in each one you can define different parameters. Here you can create them. 
    c) My projects. Here you find all the projects you have created, and you can create new projects. 
    d) Documentation. Key information so that you can get to know the tool and develop your projects.
    e) Change the language. English (en) and German (de) are supported.
    f) Profile drop-down options.
**3. Dashboard. Here is the link to create a new project or the list of current projects when they already exist.**

**4. Bottom navigation menu. Located at the bottom right of the screen. Here you will find:**
    g) Contact. General information about the project, a section where you can leave your feedback and find the link to GitHub, where you can follow the development or find useful information related to how to host the tool by yourself.
    h) Documentation. Key information so that you can get to know the tool and develop your projects.
    i) Use cases. Here you will find some cases where the functionalities of the system and its application in different projects and scenarios are presented.
    j) License. You can find the license information here.
    k) Imprint. Important information about the tool and some disclaimers are in this section.
    l) Privacy. Information on data protection, data processing and the legal and policy issues around them.



CREATE A PROJECT
^^^^^^^^^^^^^^^

To create a project in open-plan-tool, the user has three options:

.. image:: ../images/New_project_EN.png
 :width: 30%

:Empty project:
Here a project is created from scratch. When you select this option you must configure your project and for that you must include the following information: 

- Name

- Description

- Country

- Location (coordinates)

- Duration (years)

- Currency

- Discount factor

- Tax factor 

:From file:
It is also possible to load a project from a file. In this case you must include the name of the project and upload the file in json format.

:From use case:
If you want to start from one of the configured use cases, you can do so in this option. You will see a pop-up window with a link to the use cases, and a drop-down list where you can choose the use case to use. Once selected, it will appear in the "My projects" section.


CREATE A SCENARIO
^^^^^^^^^^^^^^^^^

Once the project is created, it is possible to create various scenarios within the project. To do this, we have two options: we can create a new scenario by defining all its parameters or we can load a previously created scenario from a json file.

.. image:: ../images/IMG_4_New_scenario.png
 :width: 50%

When creating a scenario from scratch, there are four steps to go through; 
1) Scenario setup, 2) Energy system design, 3) Constraints and 4) Simulation.  At the top you will see the name of the project in bold type, the name of the scenario, the four steps for scenario creation and identify which step you are in.

Maybe show the 4 steps (the top line with the 4 scenario steps) in a figure

.. image:: ../images/IMG_Scenario_Steps.png
 :width: 100%

Below is a brief description of what should be done at each step.


1) Scenario setup


The setup consists of assigning a name to the scenario, its corresponding description, the evaluated period or the number of days the simulation will run, the length of the time steps of the simulation in minutes, the start date (keep in mind that this date is important for getting the data from the time series and for plotting the data) and the fixed project costs, where the planning and development costs are included.


2) Energy system design

In this section the energy system will be designed using different components, which are located on the left panel: Providers, Production, Conversion, Storage, Demand and Bus. 
In the graphic panel drag the components you need to design your energy system, do not forget to include the buses. Note that assets must be connected to each other using a bus, and that interconnecting buses is not allowed. Connect the components together using the green and red terminals. The green terminals represent inputs, while the red terminals represent outputs, see the following example:

.. image:: ../images/IMG_example_connections.png
 :width: 100%


The components representing battery energy storage systems (BESS) have been defined with one input and one output. The BESS can be connected directly to the electrical bus; please note that the bus is supplied and feeds the battery at the same time.
.. image:: ../images/IMG_example_storage.png
 :width: 100%


When you click on the components, a screen appears where you can configure the different parameters. Each component is different, however, you will typically find three ways to complete the information: spaces to enter values, drop-down lists with default information or buttons to load time series (in this case, a graph will be displayed where the loaded data series can be previewed). Below we show you as an example some of the component setup screens, where you will have to include the parameters.


.. image:: ../images/IMG_setup_Bus.png
 :width: 100%


.. image:: ../images/IMG_setup_PV.png
 :width: 100%


.. image:: ../images/IMG_setup_HeatDemand.png
 :width: 100%


Before proceeding to the next section, be sure to complete the information requirements for each component and save the energy system.


3) Constraints

Now we must decide whether or not to activate the constraints. To do this, there is a drop-down menu in each case. The two constraints that can be defined are: 


	- **Minimal degree of autonomy**. It refers to the definition of a lower boundary on the degree of autonomy of the energy system. This factor can take values between 0 and 1, with the value close to zero showing a degree of autonomy with high dependence on the energy supplier (energy coming from the grid), while a degree of autonomy of 1 represents an autonomous energy system.


	- **Minimal share of renewables**. This constraint defines a lower boundary for the renewable share of the system, where both local generation as well as the renewable share of energy providers are taken into account. 
	
The above constraints apply to the entire system, but not to specific sectors individually.


4) Simulation

Once the scenario parameters are set, we proceed to the simulation panel. At the bottom you will find some buttons/options, where you can select whether you want to include an LP file, run the simulation and perform sensitivities. Select your preferences and get the results of your scenario.

.. image:: ../images/IMG_simulation_panel.png
 :width: 100%


SIMULATION RESULTS
^^^^^^^^^^^^^^^^^

n this screen you will find the results of your scenarios. Here it is possible to select the project [1], download the series, Key Performance Indicators (KPIs) and component costs [2], and return to the scenario setup [3]. You will then see a header with three main actions [4]: single scenarios, compare scenarios and sensitivity analysis.

.. image:: ../images/IMG_Simulation_Results_1.png
 :width: 100%

**Single scenarios**

This option makes it easy to view the results of one scenario at a time. On the left is a drop-down menu where the scenario is selected (a) and on the right is the option to add a new chart (b).


.. image:: ../images/IMG_Simulation_singleScenarios.png
 :width: 100%

Subsequently, the scenario KPIs will be presented, which include: Degree of Autonomy, Levelized costs of electricity equivalent, Onsite energy fraction, Renewable factor and Renewable share of local generation.

Then, you will be able to visualize the energy system, all its components and connections. Finally, some charts summarizing the results of the scenario are presented, including the overall cost breakdown, the energy series (in KW), the installed and optimized capacity, as well as a Sankey diagram.

Additional charts can be included, as shown in the image above with item b. The charts are interactive, as you can see the value by hovering the pointer over the chart, and there is a menu that appears in the upper right corner of the chart area. Here you can zoom in and out, reset the axes, download the image as .png format, among other options. In the legend of the charts you can select which data series to view or hide with a single click. Tables and charts can be exported in .xls, .pdf format. To do so, you can locate the three dots in the upper right corner of the tables or charts, click on them and select the alternative that suits you best.

**Compare scenarios**

It is also possible to compare the results of multiple scenarios. You only need to include the scenarios to be compared (c). Remember that you can add additional charts if necessary (b).

.. image:: ../images/IMG_Simulation_compareScenarios.png
 :width: 100%

For each scenario, a column with the values will appear in the KPI table. Also, the cost, energy and installed and optimized capacity charts show the values of the scenarios. This facilitates the comparison of the data.

As for the previous option, the charts are interactive, can be adjusted according to your needs, and both the table and the charts can be exported in different formats.

**Sensitivity analysis**

This functionality is not yet available, but you will be able to find it in a future update.


Feedback or Question
--------------------

We are happy to hear about your experience with open-plan-tool, so feel free to share your questions, comments and suggestions `here. <https://open-plan.rl-institut.de/en/user_feedback>`_ We will get back to you as soon as possible.
We also have a FAQ section, your question may already be answered there.
Remember that on the project's GitHub page you can keep track of the developments that are in progress or those that have been completed.

FAQ
---
**To be completed**