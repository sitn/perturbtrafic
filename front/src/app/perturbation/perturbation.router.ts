import { ModuleWithProviders } from '@angular/core';
import { Route, RouterModule } from '@angular/router';

import { AuthGuard } from '../guards/auth.guard';
import { FormulairePerturbationComponent } from './formulaire/formulaire-perturbation.component';
import { ListePerturbationComponent } from './liste/liste-perturbation.component';
import { AddPerturbationGuard } from '../guards/add.perturbation.guard';
import { ImpressionPerturbationComponent } from '../impression/perturbation/impression-perturbation.component';

const routes: Route[] = [
    {
        path: '',
        component: ListePerturbationComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'formulaire',
        component: FormulairePerturbationComponent,
        canActivate: [AuthGuard, AddPerturbationGuard]
    },
    {
        path: 'formulaire/view/:id',
        component: FormulairePerturbationComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'formulaire/edit/:id',
        component: FormulairePerturbationComponent,
        canActivate: [AuthGuard, AddPerturbationGuard]
    },
    {
        path: 'formulaire/print/:id',
        component: ImpressionPerturbationComponent,
        canActivate: [AuthGuard, AddPerturbationGuard]
    },
    {
        path: 'formulaire/clone/:id',
        component: FormulairePerturbationComponent,
        canActivate: [AuthGuard, AddPerturbationGuard]
    }
];

export const routing: ModuleWithProviders = RouterModule.forChild(routes);
