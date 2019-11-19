import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributsFouilleEvenementComponent } from './attributs-fouille-evenement.component';

describe('AttributsFouilleEvenementComponent', () => {
  let component: AttributsFouilleEvenementComponent;
  let fixture: ComponentFixture<AttributsFouilleEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributsFouilleEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributsFouilleEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
