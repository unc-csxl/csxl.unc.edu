/**
 * The functionality on this page abstracts out the process of pagination in the frontend so that
 * working with pagination in services and in components is significantly easier. The abstraction
 * supports simple pagination, as well as pagination where the HTTP response model does not match
 * the type of model stored in each page.
 *
 * The abstraction makes strong use of generic types so that the feature is flexible to be used
 * across the site with minimal localization.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 */

import { HttpClient } from '@angular/common/http';
import { WritableSignal, signal } from '@angular/core';
import { map, tap } from 'rxjs';

/** Defines the general model for the pagination parameters expected by the backend. */
export interface PaginationParams extends URLSearchParams {
  page: number;
  page_size: number;
  order_by: string;
  filter: string;
}

/** Defines the general model for the time range pagination parameters expected by the backend. */
export interface TimeRangePaginationParams extends URLSearchParams {
  order_by: string;
  ascending: string;
  filter: string;
  range_start: string;
  range_end: string;
}

/**
 * Interface that defines a page returned from a paginator.
 *
 * @template T: Type of data stored in the page.
 * @template ParamType: The shape of the parameters used for this page.
 */
export interface Paginated<T, ParamType> {
  items: T[];
  length: number;
  params: ParamType;
}

/**
 * This class abstracts the functionality of pagination to be significantly easier to work with across the
 * entire frontend. The paginator works across all different object types and pagination param types with
 * generics, contains functionality to convert between HTTP response models (such as `EventJson`) to regular
 * models (such as `Event`). The `page` emitted by the paginator is reactive using a signal, so data automatically
 * refreshes, simplifying data handlng in frontend components.
 *
 * @template T: Type of data stored in the paginator's pages.
 * @template Params: Type of the pagination params used by the type of object being paginated.
 */
abstract class PaginatorAbstraction<T, Params extends URLSearchParams> {
  /** Stores the previously used parameters for reference. */
  previousParams: Params | null = null;

  /** Internal writeable signal that updates when a new page is loaded. */
  private pageSignal: WritableSignal<Paginated<T, Params> | undefined> =
    signal(undefined);
  /** Signal that exposes the currently active pagination page to frontend services and components. */
  public page = this.pageSignal.asReadonly();

  /**
   * Constructs a paginator object.
   *
   * @param api: The string of the API endpoint to be called when a new page is loaded.
   */
  constructor(
    protected api: string,
    protected http: HttpClient
  ) {
    this.api = api;
  }

  /**
   * Loads a new pagination page based on the API endpoint provided in the constructor and provided
   * pagination parameters.
   *
   * Usage:
   * ```
   * paginator.loadPage<>(params);
   * paginator.page(); // Returns the loaded page.
   * ```
   *
   * This method also supports a  operator function in the case that the API endpoint returns
   * a model that is different than the provided type `T` for the paginator. This is to be most commonly
   * used with converting `Json` repsonse models to the regular typed response models. To support this,
   * the .loadPage method supports a optional generic type for the API response type.
   *
   * Usage:
   * ```
   * paginator.loadPage<EventJson>(params, parseEventJson);
   * paginator.page(); // Returns the loaded page, in type `Paginated<T>`
   * ```
   *
   * @template APIType: (Optional) Response model from the API call, if it is different than `T`.
   * @param paramStrings: Pagination parameters.
   * @param operator: (Optional) Function to convert data from `Paginated<APIType>` to `Paginated<T>`.
   */
  loadPage<APIType = T>(
    paramStrings: Params,
    operator?: ((_: APIType) => T) | null
  ) {
    // Stpres the previous pagination parameters used
    this.previousParams = paramStrings;

    // Determines the query for the URL based on the new paramateres.
    let query = new URLSearchParams(paramStrings);
    let route = this.api + '?' + query.toString();

    // Determine if an operator function is necessary
    if (operator) {
      // If so, call the API, pipe it through the operator, and update the signal.
      this.http.get<Paginated<APIType, Params>>(route).pipe(
        map((paginatedResponse) => {
          let paginated: Paginated<T, Params> = {
            items: paginatedResponse.items.map(operator),
            length: paginatedResponse.length,
            params: paginatedResponse.params
          };
          return paginated;
        }),
        tap((pageData) => this.pageSignal.set(pageData))
      );
    } else {
      // Otherwise, just call the API and update the signal.
      this.http
        .get<Paginated<T, Params>>(route)
        .pipe(tap((pageData) => this.pageSignal.set(pageData)));
    }
  }
}

/** Default paginator implementation. */
export class Paginator<T> extends PaginatorAbstraction<T, PaginationParams> {}

/** Paginator implementation for working with time ranges. */
export class TimeRangePaginator<T> extends PaginatorAbstraction<
  T,
  TimeRangePaginationParams
> {}
