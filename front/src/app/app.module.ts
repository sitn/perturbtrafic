import '@progress/kendo-angular-intl/locales/fr/all';

import { registerLocaleData, CommonModule } from '@angular/common';
import localeFr from '@angular/common/locales/fr';
import { LOCALE_ID, NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ConflitComponent } from './conflit/conflit.component';
import { CoreModule } from './core/core.module';
import { ErreurDialogComponent } from './erreur/erreur-dialog/erreur-dialog.component';
import { AuthGuard } from './guards/auth.guard';
import { GuichetCartoComponent } from './guichet-carto/guichet-carto.component';
import { LoginComponent } from './login/login.component';
import { ModeEmploiComponent } from './mode-emploi/mode-emploi.component';
import { ConfigModule, ConfigService } from './services/config.service';
import { CookieService } from './services/cookie.service';
import { EvenementFormService } from './services/evenement-form.service';
import { MapService } from './services/map.service';
import { PerturbationFormService } from './services/perturbation-form.service';
import { AppSharedModule } from './shared/shared.module';
import { InputsUtils } from './utils/inputs.utils';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { UserService } from './services/user.service';
import { AddEventGuard } from './guards/add.event.guard';
import { NotAuthorizedComponent } from './notAuthorized/not-authorized/not-authorized.component';
import { AddPerturbationGuard } from './guards/add.perturbation.guard';


registerLocaleData(localeFr);


@NgModule({
  declarations: [
    AppComponent,
    ConflitComponent,
    GuichetCartoComponent,
    ModeEmploiComponent,
    LoginComponent,
    ErreurDialogComponent,
    NotAuthorizedComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    AppSharedModule,
    AppRoutingModule,
    CoreModule
  ],
  providers: [
    AuthGuard,
    AddEventGuard,
    AddPerturbationGuard,
    ConfigService,
    ConfigModule.init(),
    CookieService,
    InputsUtils,
    { provide: LOCALE_ID, useValue: 'fr-FR' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
