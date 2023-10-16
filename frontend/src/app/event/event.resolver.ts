/**
 * The Event Resolver allows the events to be injected into the routes
 * of components.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { inject } from "@angular/core";
import { ResolveFn } from "@angular/router";
import { Event } from "./event.service"
import { EventService } from "./event.service";

export const eventResolver: ResolveFn<Event[] | undefined> = (route, state) => {
    return inject(EventService).getEvents();
}

export const eventDetailResolver: ResolveFn<Event | undefined> = (route, state) => {
    if(route.paramMap.get("id")) {
        return inject(EventService).getEvent(+route.paramMap.get("id")!);
    }
    else {
        return undefined
    }
};