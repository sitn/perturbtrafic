import { NgModule } from '@angular/core';
import { ConstanteComponent } from './constante.component';
import { ConstanteAvisPerturbationComponent } from './constante-avis-perturbation/constante-avis-perturbation.component';
import { ConstanteContactComponent } from './constante-contact/constante-contact.component';
import { ConstanteFermetureUrgenceComponent } from './constante-fermeture-urgence/constante-fermeture-urgence.component';
import { ConstanteOrganismeComponent } from './constante-organisme/constante-organisme.component';
import { ConstanteSrbComponent } from './constante-srb/constante-srb.component';
import { ConstanteUtilisateursComponent } from './constante-utilisateurs/constante-utilisateurs.component';
import { KendoUiModule } from '../shared/kendo-ui.module';
import { AppModule } from '../app.module';
import { AppSharedModule } from '../shared/shared.module';
import { routing } from './constante.router';
import { ConstanteAutorisationComponent } from './constante-autorisation/constante-autorisation.component';

@NgModule({
    imports: [
        KendoUiModule,
        AppSharedModule,
        routing
    ],
    declarations: [
        ConstanteComponent,
        ConstanteAvisPerturbationComponent,
        ConstanteContactComponent,
        ConstanteFermetureUrgenceComponent,
        ConstanteOrganismeComponent,
        ConstanteContactComponent,
        ConstanteSrbComponent,
        ConstanteUtilisateursComponent,
        ConstanteAutorisationComponent
    ],
    bootstrap: [
        ConstanteComponent
    ],
    entryComponents: [

    ]
})
export class ConstanteModule { }
