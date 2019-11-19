import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributsChantierEvenementComponent } from './attributs-chantier-evenement.component';

describe('AttributsChantierEvenementComponent', () => {
  let component: AttributsChantierEvenementComponent;
  let fixture: ComponentFixture<AttributsChantierEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributsChantierEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributsChantierEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
