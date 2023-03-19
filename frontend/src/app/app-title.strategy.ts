import { Injectable } from "@angular/core";
import { Title } from "@angular/platform-browser";
import { RouterStateSnapshot, TitleStrategy } from "@angular/router";
import { NavigationService } from "./navigation/navigation.service";

@Injectable({providedIn: 'root'})
export class AppTitleStrategy extends TitleStrategy {

    public static Provider = { provide: TitleStrategy, useClass: AppTitleStrategy };

    constructor(private readonly title: Title, private navigationService: NavigationService) {
        super();
    }

    override updateTitle(snapshot: RouterStateSnapshot) {
        let title = this.buildTitle(snapshot);
        if (title) {
            this.title.setTitle(`${title} | CS Experience Labs | CSXL at UNC-Chapel Hill`);
            this.navigationService.setTitle(title);
        } else {
            this.title.setTitle('Computer Science Experience Labs at The University of North Carolina at Chapel Hill');
            this.navigationService.setTitle('Gain Experience, Grow Community & Go Places');
        }
    }
}