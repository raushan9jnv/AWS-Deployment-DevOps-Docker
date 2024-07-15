json_data = [
    {
      "JOB_Description": "Sample JD",
      "EndClient": "Sample EndClient",
      "RequiredSkills": "SampleRequired SKILS",
      "ResumeList": [
        {
          "Id": "123",
          "Resume_URL": "Sample URL"
        },
        {
          "Id": "123",
          "Resume_URL": "SampleURL"
        }
      ]
    },
    {
      "JOB_Description": "Another JD",
      "EndClient": "Another EndClient",
      "RequiredSkills": "AnotherRequired SKILS",
      "ResumeList": [
        {
          "Id": "456",
          "Resume_URL": "Another Sample URL"
        },
        {
          "Id": "789",
          "Resume_URL": "Another SampleURL"
        }
      ]
    }
]

for job_data in json_data:
    print("\nJOB Description:", job_data["JOB_Description"])
    print("End Client:", job_data["EndClient"])
    print("Required Skills:", job_data["RequiredSkills"])
    
    # Print ResumeList for current job description
    for index, resume in enumerate(job_data["ResumeList"], start=1):
        print(f"\nResume {index}:")
        print("Id:", resume["Id"])
        print("Resume URL:", resume["Resume_URL"])
    print("*" * 100)
