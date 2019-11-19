import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { PDFExportModule } from '@progress/kendo-angular-pdf-export';

import { ContactEditionComponent } from '../contact/contact-edition-dialog/contact-edition-dialog.component';
import { MapActionsComponent } from '../map/map-actions/map-actions.component';
import { OrganismeEditionComponent } from '../organisme/organisme-edition-dialog/organisme-edition-dialog.component';
import { SaisieReperageComponent } from '../reperage/saisie-reperage/saisie-reperage.component';
import { KendoUiModule } from './kendo-ui.module';
import { MainHeaderComponent } from './main-header/main-header.component';
import { CommonModule } from '@angular/common';
import { OuiNonPipe } from '../app.pipes';

@NgModule({
    imports: [
        CommonModule,
        HttpClientModule,
        KendoUiModule,
        FormsModule,
        ReactiveFormsModule,
        PDFExportModule,
        RouterModule
    ],
    exports: [
        CommonModule,
        HttpClientModule,
        KendoUiModule,
        FormsModule,
        ReactiveFormsModule,
        PDFExportModule,
        MainHeaderComponent,
        MapActionsComponent,
        RouterModule,
        ContactEditionComponent,
        OrganismeEditionComponent,
        SaisieReperageComponent,
        OuiNonPipe,
    ],
    declarations: [
        OuiNonPipe,
        ContactEditionComponent,
        OrganismeEditionComponent,
        MainHeaderComponent,
        MapActionsComponent,
        SaisieReperageComponent
    ],
    bootstrap: [

    ],
    entryComponents: [

    ]
})
export class AppSharedModule { }
