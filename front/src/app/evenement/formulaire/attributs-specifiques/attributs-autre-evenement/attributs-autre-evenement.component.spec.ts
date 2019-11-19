import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributsAutreEvenementComponent } from './attributs-autre-evenement.component';

describe('AttributsAutreEvenementComponent', () => {
  let component: AttributsAutreEvenementComponent;
  let fixture: ComponentFixture<AttributsAutreEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributsAutreEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributsAutreEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
