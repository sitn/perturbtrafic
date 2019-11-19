import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PerturbationTypeEvenementComponent } from './perturbation-type-evenement.component';

describe('PerturbationTypeEvenementComponent', () => {
  let component: PerturbationTypeEvenementComponent;
  let fixture: ComponentFixture<PerturbationTypeEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PerturbationTypeEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PerturbationTypeEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
