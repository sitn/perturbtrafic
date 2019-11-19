import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SaisieReperageComponent } from './saisie-reperage.component';

describe('SaisieReperageComponent', () => {
  let component: SaisieReperageComponent;
  let fixture: ComponentFixture<SaisieReperageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SaisieReperageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SaisieReperageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
