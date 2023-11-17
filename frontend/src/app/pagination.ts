export interface PaginationParams {
  page: number;
  page_size: number;
  order_by: string;
  filter: string;
}

export interface EventPaginationParams {
  page: number;
  page_size: number;
  order_by: string;
  range_start: string;
  range_end: string;
}

export interface Paginated<T> {
  items: T[];
  length: number;
  params: PaginationParams;
}

export interface PaginatedEvent<T> {
  items: T[];
  length: number;
  params: EventPaginationParams;
}
