# Office Hours Technical Specification

> Authors: [Sadie Amato](https://github.com/sadieamato), [Madelyn Andrews](https://github.com/maddyandrews), [Bailey DeSouza](https://github.com/baileymeredith), [Meghan Sun](https://github.com/meghansun322)
<br> _Last Updated: 5/3/2024_

 This document contains the technical specifications for the Office Hours feature of the CSXL web application. This feature adds _4_ new database tables, _40_ new API routes, _13_ components new frontend components, and _16_ new frontend widgets to the application.

 ## Table of Contents

 * [Frontend Features](#FrontendFeatures)
     * [Office Hours Home Page](#OfficeHoursHomePage)
     * [Student Features](#StudentFeatures)
         * [Student Section Page](#StudentSectionPage)
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

The frontend features add _13_ new Angular components and _16_ new frontend widgets, all at the `/office-hours` route.
    
