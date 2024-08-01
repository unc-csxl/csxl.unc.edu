/**
 * The Event Resolver allows the events to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { EventService } from './event.service';
import { EventOverview } from './event.model';

/** This resolver injects an event into the events detail component. */
export const eventResolver: ResolveFn<EventOverview | undefined> = (
  route,
  state
) => {
  if (route.paramMap.get('id') != 'new') {
    return inject(EventService).getEvent(+route.paramMap.get('id')!);
  } else {
    return {
      id: null,
      name: '',
      time: new Date(),
      location: '',
      description: '',
      public: true,
      number_registered: 0,
      registration_limit: 0,
      organization_id: 0,
      organization_slug: '',
      organization_icon: '',
      organization_name: '',
      organizers: [],
      image_url: null,
      user_registration_type: null
    };
  }
};
