import { IAutorisations } from './IAutorisations';

export interface IUser {
    courriel: string;
    entites: {id: number, nom: string}[];
    autorisations: IAutorisations;
    currentEntity?: {id: number, nom: string};
    id: number;
    id_organisme?: number;
    login: string;
    mobile: string;
    nom: string;
    prenom: string;
    nomComplet?: string;
    telephone: string;
}

export class User implements IUser {
    courriel: string;
    entites: {id: number, nom: string}[];
    autorisations: IAutorisations;
    currentEntity?: {id: number, nom: string};
    id: number;
    id_organisme?: number;
    login: string;
    mobile: string;
    nom: string;
    prenom: string;
    nomComplet?: string;
    telephone: string;

    private _fullName: string;

    constructor(options: IUser) {
        if (options) {
            Object.assign(this, options);
        }

        this._fullName = `${this.prenom} ${this.nom}`;
    }

    get fullName() { return this._fullName; }
}


export interface IUserAD {
    uid: string;
    telephoneNumber: string;
    sn: string;
    givenName: string;
    mail: string;
    mobile: string;
    dn: string;
    id_organisme?: number;
}
