import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributsOccupationPerturbationComponent } from './attributs-occupation-perturbation.component';

describe('AttributsOccupationPerturbationComponent', () => {
  let component: AttributsOccupationPerturbationComponent;
  let fixture: ComponentFixture<AttributsOccupationPerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributsOccupationPerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributsOccupationPerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
