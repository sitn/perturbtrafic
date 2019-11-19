export interface IAxeMaintenance {
    nom?: string;
    nom_complet: string;
    position?: string;
    proprietaire: string;
    /* axe_owner: string;
    axe_name: string;
    axe_positioncode: string;
    asg_name: string; */
}

/* export class AxeMaintenance implements IAxeMaintenance {
    axe_owner: string;
    axe_name: string;
    axe_positioncode: string;
    asg_name: string;

    private _fullName: string;

    constructor(options: IAxeMaintenance) {
        if (options) {
            Object.assign(this, options);
        }

        this._fullName = `${this.axe_owner}:${this.axe_name}:${this.axe_positioncode}`;
    }

    get fullName() { return this._fullName;  }
} */
