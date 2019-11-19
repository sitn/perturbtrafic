import { ModuleWithProviders } from '@angular/core';
import { Route, RouterModule } from '@angular/router';

import { AuthGuard } from '../guards/auth.guard';
import { FormulaireEvenementComponent } from './formulaire/formulaire-evenement.component';
import { ListeEvenementComponent } from './liste/liste-evenement.component';
import { AddEventGuard } from '../guards/add.event.guard';
import { ImpressionEvenementContainerComponent } from '../impression/evenement/impression-evenement-container.component';

const routes: Route[] = [
    {
        path: '',
        component: ListeEvenementComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'formulaire',
        component: FormulaireEvenementComponent,
        canActivate: [AuthGuard, AddEventGuard]
    },
    {
        path: 'formulaire/view/:id',
        component: FormulaireEvenementComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'formulaire/edit/:id',
        component: FormulaireEvenementComponent,
        canActivate: [AuthGuard, AddEventGuard]
    },
    {
        path: 'formulaire/print/:id',
        component: ImpressionEvenementContainerComponent, canActivate: [AuthGuard]
    },
    {
        path: 'formulaire/print_folder/:id',
        component: ImpressionEvenementContainerComponent, canActivate: [AuthGuard]
    },
];


export const routing: ModuleWithProviders = RouterModule.forChild(routes);
