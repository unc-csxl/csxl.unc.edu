
export interface PaginationParams {
    page: number;
    page_size: number;
    order_by: string;
    filter: string;
}

export interface Paginated<T> {
    items: T[];
    length: number;
    params: PaginationParams;
}