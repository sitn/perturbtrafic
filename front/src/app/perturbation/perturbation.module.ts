import { NgModule } from '@angular/core';

import { AppSharedModule } from '../shared/shared.module';
import {
    AttributsFermeturePerturbationComponent,
} from './formulaire/attributs-specifiques/attributs-fermeture-perturbation/attributs-fermeture-perturbation.component';
import {
    AttributsOccupationPerturbationComponent,
} from './formulaire/attributs-specifiques/attributs-occupation-perturbation/attributs-occupation-perturbation.component';
import { CartePerturbationComponent } from './formulaire/carte-perturbation/carte-perturbation.component';
import {
    InformationsPerturbationComponent,
} from './formulaire/informations-perturbation/informations-perturbation.component';
import {
    PerturbationTypeEvenementComponent,
} from './formulaire/perturbation-type-evenement/perturbation-type-evenement.component';
import { RemarquePerturbationComponent } from './formulaire/remarque-perturbation/remarque-perturbation.component';
import { TypePerturbationComponent } from './formulaire/type-perturbation/type-perturbation.component';
import { ListePerturbationComponent } from './liste/liste-perturbation.component';
import { RecherchePerturbationComponent } from './liste/recherche/recherche-perturbation.component';
import { ResultatsPerturbationComponent } from './liste/resultats/resultats-perturbation.component';
import { FormulairePerturbationComponent } from './formulaire/formulaire-perturbation.component';
import { AvisPerturbationComponent } from './formulaire/avis-perturbation/avis-perturbation.component';
import { routing } from './perturbation.router';
import { PDFModule, ExcelModule } from '@progress/kendo-angular-grid';
import { MapService } from '../services/map.service';
import { PerturbationFormService } from '../services/perturbation-form.service';
import { ImpressionPerturbationComponent } from '../impression/perturbation/impression-perturbation.component';
import { OuiNonPipe } from '../app.pipes';


@NgModule({
    imports: [
        AppSharedModule,
        routing,
        PDFModule,
        ExcelModule
    ],
    declarations: [
        FormulairePerturbationComponent,
        AvisPerturbationComponent,
        RecherchePerturbationComponent,
        ResultatsPerturbationComponent,
        ListePerturbationComponent,
        PerturbationTypeEvenementComponent,
        ImpressionPerturbationComponent,
        TypePerturbationComponent,
        InformationsPerturbationComponent,
        AttributsFermeturePerturbationComponent,
        AttributsOccupationPerturbationComponent,
        CartePerturbationComponent,
        RemarquePerturbationComponent,
    ],
    exports: [
    ],
    providers: [
        MapService,
        PerturbationFormService
    ],
    bootstrap: [
    ],
    entryComponents: [

    ]
})
export class PerturbationModule { }
