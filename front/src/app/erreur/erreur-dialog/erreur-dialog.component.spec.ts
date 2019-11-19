import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ErreurPopupComponent } from './erreur-dialog.component';

describe('ErreurPopupComponent', () => {
  let component: ErreurPopupComponent;
  let fixture: ComponentFixture<ErreurPopupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ErreurPopupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ErreurPopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
