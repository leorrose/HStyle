import { TeamMember } from './../models/team-member';
import { TeamMembersComponent } from './../team-members/team-members.component';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TeamMemberCardComponent } from './team-member-card.component';
import { NO_ERRORS_SCHEMA } from '@angular/core';

describe('TeamMemberCardComponent', () => {
    let component: TeamMemberCardComponent;
    let fixture: ComponentFixture<TeamMemberCardComponent>;
    const teamMemberMock: TeamMember = { name: 'test', imagePath: 'test',
                                       description: `test`, researchgateLink: 'test',
                                       linkedinLink: 'test', githubLink: 'test',
                                       emailAddress: 'test'
    };

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [TeamMemberCardComponent],
            schemas: [NO_ERRORS_SCHEMA]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(TeamMemberCardComponent);
        component = fixture.componentInstance;
        component.teamMember = teamMemberMock;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    // it('should run the copy command', (done) => {
    //     spyOn(document, 'execCommand');
    //     component.copyToClipBoard('copied text');
    //     expect(document.execCommand).toHaveBeenCalledWith('copy');

    //     navigator.clipboard.readText().then(text => {
    //       expect(text).toBe('copied text');
    //       done();
    //     })
    //     .catch(err => {
    //       fail(err);
    //     });
    // });
});
