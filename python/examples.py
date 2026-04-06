"""Example usage of the Kairos SDK.

These are practical examples showing how to use the SDK in real scenarios.
"""

import asyncio
from kairos import Kairos, KairosSync
from kairos.errors import NotFoundError, AuthError


# ============================================================================
# ASYNC EXAMPLES
# ============================================================================


async def async_list_tasks_example():
    """List all tasks with pagination."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        # Get first page of tasks
        result = await kairos.tasks.list(page=1, limit=20)

        print(f"Found {result.pagination.total} total tasks")
        print(f"Page {result.pagination.page} of {result.pagination.total}")

        for task in result.data:
            print(f"- {task.title} ({task.status})")

        # Continue to next page if available
        if result.pagination.has_more:
            next_page = await kairos.tasks.list(
                page=result.pagination.page + 1, limit=20
            )


async def async_create_goal_with_tasks_example():
    """Create a goal and add multiple tasks to it."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        # Create a goal
        goal = await kairos.goals.create(
            title="Q1 2024 Engineering Goals",
            description="Main engineering objectives for Q1",
            status="active",
            due_date="2024-03-31",
        )
        print(f"Created goal: {goal.id} - {goal.title}")

        # Create tasks for this goal
        task_titles = [
            "Set up CI/CD pipeline",
            "Implement authentication",
            "Write API documentation",
        ]

        for i, title in enumerate(task_titles, 1):
            task = await kairos.tasks.create(
                title=title,
                goal_id=goal.id,
                priority="high",
                estimated_hours=float(8 + i * 2),
            )
            print(f"  Created task: {task.id} - {task.title}")

        # List tasks for the goal
        goal_tasks = await kairos.goals.list_tasks(goal.id)
        print(f"\nGoal has {len(goal_tasks.data)} tasks")


async def async_update_task_workflow_example():
    """Simulate moving a task through a workflow."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        try:
            # Get a task
            task = await kairos.tasks.get("task_123")
            print(f"Current status: {task.status}")

            # Move through workflow
            statuses = ["in_progress", "in_review", "completed"]
            for status in statuses:
                updated = await kairos.tasks.update(task.id, status=status)
                print(f"Updated status to: {updated.status}")

                # Add a comment
                comment = await kairos.tasks.add_comment(
                    task.id, f"Status changed to {status}"
                )
                print(f"  Added comment: {comment.id}")

        except NotFoundError as e:
            print(f"Task not found: {e.message}")


async def async_team_analysis_example():
    """Analyze team and member information."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        # Get team info
        team = await kairos.team.get()
        print(f"Team: {team.name} ({team.slug})")
        print(f"Description: {team.description}")

        # List members
        members = await kairos.team.list_members(limit=100)
        print(f"\nTeam Members ({len(members.data)}):")

        for member in members.data:
            print(f"  - {member.name} ({member.email})")
            print(f"    Role: {member.role}")
            print(f"    Joined: {member.joined_at}")


async def async_document_retrieval_example():
    """Retrieve and display documents."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        # List all documents
        docs = await kairos.documents.list(limit=50)
        print(f"Found {docs.pagination.total} documents\n")

        # Display first few
        for doc in docs.data[:5]:
            print(f"Document: {doc.title}")
            print(f"  ID: {doc.id}")
            print(f"  Created: {doc.created_at}")
            if doc.content:
                preview = doc.content[:100] + "..." if len(doc.content) > 100 else doc.content
                print(f"  Preview: {preview}")
            print()


async def async_error_handling_example():
    """Demonstrate error handling."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        try:
            # Try to get a task that doesn't exist
            task = await kairos.tasks.get("nonexistent_id")

        except NotFoundError as e:
            print(f"Task not found (404)")
            print(f"  Code: {e.code}")
            print(f"  Message: {e.message}")
            print(f"  Request ID: {e.request_id}")

        try:
            # Try with invalid API key (would be caught during client init)
            pass

        except AuthError as e:
            print(f"Authentication failed (401)")
            print(f"  Message: {e.message}")


async def main():
    """Run all async examples (commented out except documentation)."""
    # Uncomment examples to run them with valid API key
    # await async_list_tasks_example()
    # await async_create_goal_with_tasks_example()
    # await async_update_task_workflow_example()
    # await async_team_analysis_example()
    # await async_document_retrieval_example()
    # await async_error_handling_example()
    print("Async examples defined. Uncomment in main() to run.")


# ============================================================================
# SYNC EXAMPLES
# ============================================================================


def sync_list_tasks_example():
    """List all tasks synchronously."""
    with KairosSync(api_key="kairos_sk_...") as kairos:
        result = kairos.tasks.list(page=1, limit=20)

        print(f"Found {result.pagination.total} total tasks")

        for task in result.data:
            print(f"- {task.title} ({task.status})")


def sync_batch_task_update_example():
    """Update multiple tasks at once."""
    with KairosSync(api_key="kairos_sk_...") as kairos:
        # Get all pending tasks
        tasks = kairos.tasks.list(status="to_do", limit=100)

        print(f"Found {len(tasks.data)} pending tasks")

        # Update them
        for task in tasks.data:
            updated = kairos.tasks.update(
                task.id,
                status="in_progress",
                assigned_to="user_123",  # Assign to someone
            )
            print(f"Updated: {updated.title}")


def sync_get_auth_info_example():
    """Get information about current API key."""
    with KairosSync(api_key="kairos_sk_...") as kairos:
        me = kairos.me()

        print(f"Team ID: {me.team_id}")
        print(f"Scopes: {', '.join(me.scopes)}")
        print(f"Rate Limit: {me.rate_limit_per_minute} requests/minute")
        print(f"Rate Limit: {me.rate_limit_per_hour} requests/hour")


def sync_comment_workflow_example():
    """Add comments and track discussion on a task."""
    with KairosSync(api_key="kairos_sk_...") as kairos:
        try:
            task = kairos.tasks.get("task_123")
            print(f"Task: {task.title}\n")

            # Add comments
            comments = [
                "Starting work on this",
                "@alice can you review the approach?",
                "Updated based on feedback",
                "Ready for merge",
            ]

            for comment_text in comments:
                comment = kairos.tasks.add_comment(task.id, comment_text)
                print(f"Added comment: {comment_text}")

            # List all comments
            all_comments = kairos.tasks.list_comments(task.id)
            print(f"\nTotal comments: {all_comments.pagination.total}")

        except NotFoundError:
            print("Task not found")


# ============================================================================
# PATTERN EXAMPLES
# ============================================================================


async def async_pagination_pattern_example():
    """Pattern for iterating through all results with pagination."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        page = 1
        limit = 20
        all_tasks = []

        while True:
            result = await kairos.tasks.list(page=page, limit=limit)

            all_tasks.extend(result.data)
            print(f"Loaded page {page}: {len(result.data)} items")

            if not result.pagination.has_more:
                break

            page += 1

        print(f"Total tasks loaded: {len(all_tasks)}")


async def async_bulk_operations_pattern_example():
    """Pattern for bulk operations on multiple items."""
    async with Kairos(api_key="kairos_sk_...") as kairos:
        # Create multiple tasks
        task_ids = []
        for i in range(5):
            task = await kairos.tasks.create(
                title=f"Bulk Task {i+1}",
                priority="medium",
            )
            task_ids.append(task.id)
            print(f"Created: {task.id}")

        # Update all of them
        print("\nUpdating all tasks...")
        for task_id in task_ids:
            await kairos.tasks.update(
                task_id,
                status="in_progress",
                priority="high",
            )
            print(f"Updated: {task_id}")

        # Delete all of them
        print("\nDeleting all tasks...")
        for task_id in task_ids:
            await kairos.tasks.delete(task_id)
            print(f"Deleted: {task_id}")


if __name__ == "__main__":
    # Run async examples
    asyncio.run(main())

    # Uncomment to run sync examples with valid API key
    # sync_list_tasks_example()
    # sync_batch_task_update_example()
    # sync_get_auth_info_example()
    # sync_comment_workflow_example()
