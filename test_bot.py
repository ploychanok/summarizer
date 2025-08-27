#!/usr/bin/env python3
"""
Test Script for Summarizer
Validates functionality with sample data without requiring API keys
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.message_parser import MessageParser
from utils.summary_formatter import SummaryFormatter
from services.ai_service import AIService


def test_message_parser():
    """Test the message parser with sample data."""
    print("🧪 Testing Message Parser...")
    
    parser = MessageParser()
    
    sample_messages = [
        {
            "user": "U123",
            "text": "Hey team, I think we should go with Option B for the API integration. What do you all think?",
            "ts": "1640995200.000100"
        },
        {
            "user": "U456",
            "text": "I agree with <@U123>. Option B seems more scalable. <@U789> can you create a JIRA ticket for this by Friday?",
            "ts": "1640995260.000200"
        },
        {
            "user": "U789",
            "text": "I'll take care of the JIRA ticket by end of day. Should we also update the timeline?",
            "ts": "1640995320.000300"
        },
        {
            "user": "U123",
            "text": "Decision: We are going with Option B. Bob will handle the JIRA ticket.",
            "ts": "1640995380.000400"
        },
        {
            "user": "U456",
            "text": "What about the testing timeline? Do we have enough QA resources for the next sprint?",
            "ts": "1640995440.000500"
        },
        {
            "user": "U789",
            "text": "Action item: I need to check with the QA team and report back by tomorrow.",
            "ts": "1640995500.000600"
        }
    ]
    
    user_lookup = {
        "U123": "Alice",
        "U456": "Carol",
        "U789": "Bob"
    }
    
    # Parse messages
    parsed_messages = parser.parse_messages(sample_messages, user_lookup)
    
    print("Parsed Messages:")
    for i, msg in enumerate(parsed_messages, 1):
        print(f"  {i}. {msg['user_name']}: {msg['clean_text']}")
        print(f"     Decision: {msg['is_decision']} | Action: {msg['is_action_item']} | Question: {msg['is_question']}")
        if msg['mentions']:
            mentions = [m['name'] for m in msg['mentions']]
            print(f"     Mentions: {', '.join(mentions)}")
    
    # Get statistics
    stats = parser.get_message_stats(parsed_messages)
    print(f"\nMessage Statistics:")
    print(f"  Total: {stats['total']}")
    print(f"  Decisions: {stats['decisions']}")
    print(f"  Actions: {stats['actions']}")
    print(f"  Questions: {stats['questions']}")
    print(f"  With mentions: {stats['with_mentions']}")
    print(f"  With deadlines: {stats['with_deadlines']}")
    
    return parsed_messages, user_lookup


def test_summary_formatter(sample_summary=None):
    """Test the summary formatter."""
    print("\n🎨 Testing Summary Formatter...")
    
    formatter = SummaryFormatter()
    
    # Use provided summary or create a mock one
    if sample_summary is None:
        sample_summary = {
            "decisions": [
                "Agreed to proceed with Option B for the API integration",
                "Bob will handle the JIRA ticket creation"
            ],
            "action_items": [
                "@Bob: Create JIRA ticket for API integration Option B (Due: Friday)",
                "@Bob: Check with QA team and report back (Due: tomorrow)"
            ],
            "questions": [
                "Should we also update the timeline?",
                "Do we have enough QA resources for the next sprint?"
            ],
            "key_points": [
                "Discussion about API integration options",
                "Resource planning for upcoming sprint",
                "Timeline considerations for development"
            ]
        }
    
    context = {
        "channel_name": "test-channel",
        "message_count": 6,
        "participant_count": 3,
        "timeframe": "test conversation"
    }
    
    # Test thread summary formatting
    thread_summary = formatter.format_thread_summary(sample_summary, context)
    print("Thread Summary Format:")
    print(thread_summary)
    
    # Test quick summary
    quick_summary = formatter.format_quick_summary(sample_summary)
    print(f"\nQuick Summary: {quick_summary}")
    
    # Test summary statistics
    stats = formatter.get_summary_stats(sample_summary)
    print(f"\nSummary Stats: {stats}")
    
    return sample_summary


async def test_ai_service_patterns():
    """Test AI service with pattern-based fallback."""
    print("\n🤖 Testing AI Service (Pattern-based fallback)...")
    
    # Test without API key to trigger pattern-based summary
    ai_service = AIService("fake-api-key")
    
    sample_messages = [
        {
            "user": "U123",
            "user_name": "Alice",
            "text": "Decision: We are going with Option B for the API integration",
            "clean_text": "Decision: We are going with Option B for the API integration",
            "is_decision": True,
            "is_action_item": False,
            "is_question": False,
            "mentions": [],
            "extracted_deadline": None,
            "ts": "1640995200.000100"
        },
        {
            "user": "U789",
            "user_name": "Bob",
            "text": "I'll create the JIRA ticket by Friday",
            "clean_text": "I'll create the JIRA ticket by Friday",
            "is_decision": False,
            "is_action_item": True,
            "is_question": False,
            "mentions": [],
            "extracted_deadline": "by Friday",
            "ts": "1640995320.000300"
        },
        {
            "user": "U456",
            "user_name": "Carol",
            "text": "What about the testing timeline?",
            "clean_text": "What about the testing timeline?",
            "is_decision": False,
            "is_action_item": False,
            "is_question": True,
            "mentions": [],
            "extracted_deadline": None,
            "ts": "1640995440.000500"
        }
    ]
    
    try:
        # This will fail to OpenAI but should fallback to pattern-based
        summary = await ai_service.summarize_conversation(sample_messages)
        print("Pattern-based summary generated:")
        for key, items in summary.items():
            print(f"  {key}: {len(items)} items")
            for item in items[:2]:  # Show first 2 items
                print(f"    - {item}")
        return summary
    except Exception as e:
        print(f"AI Service test failed: {e}")
        return None


def test_integration():
    """Test integration of all components."""
    print("\n🔗 Testing Integration...")
    
    # Parse messages
    parsed_messages, user_lookup = test_message_parser()
    
    # Create a mock summary (simulating AI processing)
    mock_summary = {
        "decisions": [
            "Decision: We are going with Option B. Bob will handle the JIRA ticket"
        ],
        "action_items": [
            "@Bob: Create JIRA ticket for API integration Option B (Due: Friday)",
            "@Bob: Check with QA team and report back (Due: tomorrow)"
        ],
        "questions": [
            "What do you all think about Option B?",
            "Should we also update the timeline?",
            "What about the testing timeline? Do we have enough QA resources for the next sprint?"
        ],
        "key_points": [
            "Discussion about API integration options",
            "Timeline and resource planning considerations"
        ]
    }
    
    # Format the summary
    formatted_summary = test_summary_formatter(mock_summary)
    
    print("\n✅ Integration test completed successfully!")
    return True


def test_error_handling():
    """Test error handling scenarios."""
    print("\n🚨 Testing Error Handling...")
    
    parser = MessageParser()
    formatter = SummaryFormatter()
    
    # Test with empty messages
    empty_result = parser.parse_messages([], {})
    assert empty_result == [], "Should handle empty message list"
    
    # Test with malformed messages
    malformed_messages = [
        {},  # Empty message
        {"user": "U123"},  # Missing text
        {"text": "Hello world"},  # Missing user
    ]
    
    parsed = parser.parse_messages(malformed_messages, {})
    assert len(parsed) == 3, "Should handle malformed messages"
    
    # Test formatter with empty summary
    empty_summary = {}
    formatted = formatter.format_thread_summary(empty_summary, {
        "channel_name": "test",
        "message_count": 0,
        "participant_count": 0
    })
    assert "None identified" in formatted, "Should handle empty summary"
    
    print("Error handling tests passed!")


def main():
    """Main test function."""
    print("🧪 Testing Summarizer Bot...\n")
    
    try:
        # Run individual component tests
        test_message_parser()
        test_summary_formatter()
        
        # Test AI service (pattern-based fallback)
        import asyncio
        asyncio.run(test_ai_service_patterns())
        
        # Test error handling
        test_error_handling()
        
        # Test integration
        test_integration()
        
        print("\n✅ All tests completed successfully!")
        
        # Show usage instructions
        print("\n📖 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up environment variables in .env file")
        print("3. Create Slack app and get API tokens")
        print("4. Run the bot: python src/main.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)