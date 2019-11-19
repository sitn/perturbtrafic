import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributsManifestationEvenementComponent } from './attributs-manifestation-evenement.component';

describe('AttributsManifestationEvenementComponent', () => {
  let component: AttributsManifestationEvenementComponent;
  let fixture: ComponentFixture<AttributsManifestationEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributsManifestationEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributsManifestationEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
