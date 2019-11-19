import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NouvelOrganismeComponent } from './organisme-edition-dialog.component';

describe('NouvelOrganismeComponent', () => {
  let component: NouvelOrganismeComponent;
  let fixture: ComponentFixture<NouvelOrganismeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NouvelOrganismeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NouvelOrganismeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
