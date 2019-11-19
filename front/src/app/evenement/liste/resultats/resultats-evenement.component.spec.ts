import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EvenementResultatComponent } from './resultats-evenement.component';

describe('EvenementResultatComponent', () => {
  let component: EvenementResultatComponent;
  let fixture: ComponentFixture<EvenementResultatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EvenementResultatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EvenementResultatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
