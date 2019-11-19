import { NgModule } from '@angular/core';

import { FormulairePerturbationComponent } from '../perturbation/formulaire/formulaire-perturbation.component';
import { AppSharedModule } from '../shared/shared.module';
import {
    AttributsAutreEvenementComponent,
} from './formulaire/attributs-specifiques/attributs-autre-evenement/attributs-autre-evenement.component';
import {
    AttributsChantierEvenementComponent,
} from './formulaire/attributs-specifiques/attributs-chantier-evenement/attributs-chantier-evenement.component';
import {
    AttributsFouilleEvenementComponent,
} from './formulaire/attributs-specifiques/attributs-fouille-evenement/attributs-fouille-evenement.component';
import {
    AttributsManifestationEvenementComponent,
} from './formulaire/attributs-specifiques/attributs-manifestation-evenement/attributs-manifestation-evenement.component';
import { CarteEvenementComponent } from './formulaire/carte-evenement/carte-evenement.component';
import { ConflitsEvenementComponent } from './formulaire/conflits-evenement/conflits-evenement.component';
import { FormulaireEvenementComponent } from './formulaire/formulaire-evenement.component';
import { InformationsEvenementComponent } from './formulaire/informations-evenement/informations-evenement.component';
import { RemarqueEvenementComponent } from './formulaire/remarque-evenement/remarque-evenement.component';
import { TypeEvenementComponent } from './formulaire/type-evenement/type-evenement.component';
import { ListeEvenementComponent } from './liste/liste-evenement.component';
import { RechercheEvenementComponent } from './liste/recherche/recherche-evenement.component';
import { ResultatsEvenementComponent } from './liste/resultats/resultats-evenement.component';
import { EvenementEcheanceComponent } from './evenement-echeance/evenement-echeance.component';
import { routing } from './evenement.router';
import { PDFModule, ExcelModule } from '@progress/kendo-angular-grid';
import { MapService } from '../services/map.service';
import { EvenementFormService } from '../services/evenement-form.service';
import { ImpressionEvenementComponent } from '../impression/evenement/impression-evenement.component';
import { ImpressionEvenementContainerComponent } from '../impression/evenement/impression-evenement-container.component';


@NgModule({
    imports: [
        AppSharedModule,
        routing,
        PDFModule,
        ExcelModule
    ],
    declarations: [
        FormulaireEvenementComponent,
        ListeEvenementComponent,
        RechercheEvenementComponent,
        ResultatsEvenementComponent,
        CarteEvenementComponent,
        TypeEvenementComponent,
        RemarqueEvenementComponent,
        ConflitsEvenementComponent,
        InformationsEvenementComponent,
        AttributsChantierEvenementComponent,
        AttributsManifestationEvenementComponent,
        AttributsAutreEvenementComponent,
        AttributsFouilleEvenementComponent,
        EvenementEcheanceComponent,
        ImpressionEvenementComponent,
        ImpressionEvenementContainerComponent
    ],
    exports: [
        ListeEvenementComponent
    ],
    providers: [
        MapService,
        EvenementFormService
    ],
    bootstrap: [
    ],
    entryComponents: [

    ]
})
export class EvenementModule { }
