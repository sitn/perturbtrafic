import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributsFermeturePerturbationComponent } from './attributs-fermeture-perturbation.component';

describe('AttributsFermeturePerturbationComponent', () => {
  let component: AttributsFermeturePerturbationComponent;
  let fixture: ComponentFixture<AttributsFermeturePerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributsFermeturePerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributsFermeturePerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
