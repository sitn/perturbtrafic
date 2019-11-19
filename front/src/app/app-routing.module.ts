import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ConflitComponent } from './conflit/conflit.component';
import { AuthGuard } from './guards/auth.guard';
import { GuichetCartoComponent } from './guichet-carto/guichet-carto.component';
import { LoginComponent } from './login/login.component';
import { ModeEmploiComponent } from './mode-emploi/mode-emploi.component';
import { NotAuthorizedComponent } from './notAuthorized/not-authorized/not-authorized.component';

const routes: Routes = [
  { path: 'Forbidden', component: NotAuthorizedComponent },
  { path: 'login', component: LoginComponent },
  { path: 'evenements', loadChildren: './evenement/evenement.module#EvenementModule', canActivate: [AuthGuard] },
  {
    path: 'perturbations',
    loadChildren: './perturbation/perturbation.module#PerturbationModule', canActivate: [AuthGuard]
  },
  { path: 'conflits', component: ConflitComponent, canActivate: [AuthGuard] },
  {
    path: 'constantes', canActivate: [AuthGuard],
    loadChildren: './constante/constante.module#ConstanteModule'
  },
  { path: 'guichet-carto', component: GuichetCartoComponent, canActivate: [AuthGuard] },
  { path: 'mode-emploi', component: ModeEmploiComponent, canActivate: [AuthGuard] },
  { path: '', pathMatch: 'full', redirectTo: '/evenements' }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      scrollPositionRestoration: 'enabled'
    })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
