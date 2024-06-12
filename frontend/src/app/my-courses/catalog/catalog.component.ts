import { Component } from '@angular/core';

@Component({
  selector: 'app-catalog',
  templateUrl: './catalog.component.html',
  styleUrls: ['./catalog.component.css']
})
export class CatalogComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'catalog',
    title: 'Catalog',
    component: CatalogComponent
  };

  /** Links for the tab bar */
  public links = [
    {
      label: 'Current Offerings',
      path: '/catalog/offerings',
      icon: 'overview'
    },
    { label: 'All Courses', path: '/catalog/all', icon: 'list_alt' }
  ];
}
