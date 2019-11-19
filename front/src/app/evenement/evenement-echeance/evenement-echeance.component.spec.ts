import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EvenementEcheanceComponent } from './evenement-echeance.component';

describe('EvenementEcheanceComponent', () => {
  let component: EvenementEcheanceComponent;
  let fixture: ComponentFixture<EvenementEcheanceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EvenementEcheanceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EvenementEcheanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
