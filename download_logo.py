import requests
import os

url = "https://private-us-east-1.manuscdn.com/sessionFile/7WQIT6oGjMXsjBnwKaIYoQ/sandbox/HB6Nncf6KBgKila2PIbo31_1764241841566_na1fn_L2hvbWUvdWJ1bnR1L3JhaGhhbF9sb2dvX2ljb24.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvN1dRSVQ2b0dqTVhzakJud0thSVlvUS9zYW5kYm94L0hCNk5uY2Y2S0JnS2lsYTJQSWJvMzFfMTc2NDI0MTg0MTU2Nl9uYTFmbl9MMmh2YldVdmRXSjFiblIxTDNKaGFHaGhiRjlzYjJkdlgybGpiMjQucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=W9nAqUn6sXc-fdA8QD8u40Rz4QBCs7qBKybQReeAZXP6jDSFBjQA3kCVbDXsJMKBt2dm~2arB~-a0y7~KbE5z4TtF32Gk2jH~8l8HezGF9cuMfieKdXVVrvA17zRmPCKhM91WjRUtHpt~Ly6WID5m4tB3AvSO-Mm0biETq97JNEpIvvdpluai6w-~p0dgaTu1xDxcp1Eh6BNmjhQgjmAcWiMQtUGHDtApR6yWawWWG0vn6WtCHBhJKNrlkVQoL8KxW81Hp0e0-ztqhSe0fh3edW3kErpJEf6jn36Rvhhtbssb-B~kQBejSiaWMz~SxtceIS4uSKfuEWeDJzye0eazA__"
output_dir = "src/app/assets"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "rahhal_logo.png")

try:
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Image saved to {output_path}")
except Exception as e:
    print(f"Failed to download image: {e}")
