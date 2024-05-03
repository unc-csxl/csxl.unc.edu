# Office Hours Technical Specification

> Authors: [Sadie Amato](https://github.com/sadieamato), [Madelyn Andrews](https://github.com/maddyandrews), [Bailey DeSouza](https://github.com/baileymeredith), [Meghan Sun](https://github.com/meghansun322)
<br> _Last Updated: 5/3/2024_

 This document contains the technical specifications for the Office Hours feature of the CSXL web application. This feature adds _4_ new database tables, _40_ new API routes, _13_ components new frontend components, and _16_ new frontend widgets to the application.

 ## Table of Contents

 * [Frontend Features](#FrontendFeatures)
     * [Office Hours Home Page](#OfficeHoursHomePage)
     * [Student Features](#StudentFeatures)
         * [Student Section Home](#StudentSectionHome)
         * [Ticket Creation](#TicketCreation)
         * [History Tab](#HistoryTab)
     * [TA Features](#TAFeatures)
         * [TA Section Page](#TASectionPage)
         * [Ticket Queue Page](#TicketQueuePage)
         * [Event Feature](#EventFeature)
         * [History Tab](#HistoryTab)
     * [Instructor Features](#InstructorFeatures)
         * [Creating a Section](#CreatingASection)
         * [Instructor Section Page](#InstructorSectionPage)
         * [Data Tab](#DataTab)
         * [People Tab](#PeopleTab)
     * [GTA Features](#GTAFeatures)
* [Backend Design and Implementation](#BackendDesignandImplementation)
	* [Entity Design](#EntityDesign)
	* [Pydantic Model Implementation](#PydanticModelImplementation)
	* [API Implementation](#APIImplementation)
	* [Permission Summary](#PermissionSummary)
	* [Testing](#Testing)

## Frontend Features<a name='FrontendFeatures'></a>

The frontend features add _13_ new Angular components and _16_ new frontend widgets, all at the `/office-hours` route. All features are only accessible to _authenticated users_ of the CSXL.

### Office Hours Home Page <a name='OfficeHoursHomePage'></a>

The following page has been added as the home page of our Office Hours Feature.
![Office Hours Home Page](../images/specs/office-hours/oh-home.png)

The home page for the new Office Hours feature is available on the side navigation toolbar at `/office-hours`. The home page contains a list of a user's Office Hours sections viewable by term.

### Student Features<a name='StudentFeatures'></a>

The following pages have been added and are available for users with the Student role for an AcademicSection. These pages are ultimately powered by new Angular service functions connected to new backend APIs.
    
#### Student Section Home<a name='Student Section Home'></a>

