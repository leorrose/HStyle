import { TeamMemberCardComponent } from './../team-member-card/team-member-card.component';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TeamMembersComponent } from './team-members.component';
import { TeamMemberService } from '../services/team-member.service';
import { NO_ERRORS_SCHEMA } from '@angular/core';

describe('TeamMembersComponent', () => {
    let component: TeamMembersComponent;
    let fixture: ComponentFixture<TeamMembersComponent>;
    const TeamMemberServiceMock: any = jasmine.createSpyObj('teamMemberService', ['getTeamMembers']);

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [
                TeamMembersComponent,
                TeamMemberCardComponent
            ],
            providers: [
                { provide: TeamMemberService, useValue: TeamMemberServiceMock}
            ],
            schemas: [NO_ERRORS_SCHEMA]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(TeamMembersComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();

        // mock
        TeamMemberServiceMock.getTeamMembers.and.returnValue([]);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
        expect(TeamMemberServiceMock.getTeamMembers).toHaveBeenCalled();
        expect(component.teamMembers).toEqual([]);
    });

    it('should split non empty team members array into chunks', () => {
        const teamMember1 = { name: 'test1', imagePath: 'test1',
                              description: `test1`, researchgateLink: 'test1',
                              linkedinLink: 'test1', githubLink: 'test1',
                              emailAddress: 'test1',
        };
        const teamMember2 = { name: 'test2', imagePath: 'test2',
                              description: `test2`, researchgateLink: 'test2',
                              linkedinLink: 'test2', githubLink: 'test2',
                              emailAddress: 'test2',
        };
        const teamMember3 = { name: 'test3', imagePath: 'test3',
                              description: `test3`, researchgateLink: 'test3',
                              linkedinLink: 'test3', githubLink: 'test3',
                              emailAddress: 'test3',
        };
        const teamMember4 = { name: 'test4', imagePath: 'test4',
                              description: `test4`, researchgateLink: 'test4',
                              linkedinLink: 'test4', githubLink: 'test4',
                              emailAddress: 'test4',
        };
        const teamMember5 = { name: 'test5', imagePath: 'test5',
                              description: `test5`, researchgateLink: 'test5',
                              linkedinLink: 'test5', githubLink: 'test5',
                              emailAddress: 'test5',
        };
        const teamMember6 = { name: 'test6', imagePath: 'test6',
                              description: `test6`, researchgateLink: 'test6',
                              linkedinLink: 'test6', githubLink: 'test6',
                              emailAddress: 'test6',
        };

        expect(component.chunkArray([teamMember1, teamMember2, teamMember3, teamMember4, teamMember5, teamMember6], 2)).toEqual(
            [[teamMember1, teamMember2], [teamMember3, teamMember4], [teamMember5, teamMember6]]
        );

        expect(component.chunkArray([teamMember1, teamMember2, teamMember3, teamMember4, teamMember5, teamMember6], 3)).toEqual(
            [[teamMember1, teamMember2, teamMember3], [teamMember4, teamMember5, teamMember6]]
        );

        expect(component.chunkArray([teamMember1, teamMember2, teamMember3, teamMember4, teamMember5, teamMember6], 4)).toEqual(
            [[teamMember1, teamMember2, teamMember3, teamMember4], [teamMember5, teamMember6, Object({  }), Object({  })]]
        );
    });


    it('should split empty team members array into chunks', () => {
        expect(component.chunkArray([], 2)).toEqual([]);
    });
});
